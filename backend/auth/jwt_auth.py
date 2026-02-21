"""
JWT認証モジュール
JWTトークンの生成・検証を実装
"""
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import (Depends, HTTPException, WebSocket, WebSocketException,
                     status)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer認証
security = HTTPBearer()

# JWT設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JWTAuth:
    """JWT認証クラス"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """パスワードの検証"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """パスワードのハッシュ化"""
        # bcryptの72バイト制限に対応
        if password is None:
            raise ValueError("Password cannot be None")

        # 文字列をバイトに変換して長さチェック
        if isinstance(password, str):
            password_bytes = password.encode("utf-8")
            if len(password_bytes) > 72:
                # 72バイトを超える場合は切り詰め
                password_bytes = password_bytes[:72]
                password = password_bytes.decode("utf-8", errors="ignore")

        try:
            return pwd_context.hash(password)
        except (ValueError, AttributeError) as e:
            # bcrypt/passlibの互換性エラーを処理
            error_msg = str(e)
            if "longer than 72 bytes" in error_msg:
                # 72バイトを超える場合
                password_bytes = password.encode("utf-8")[:72]
                password = password_bytes.decode("utf-8", errors="ignore")
                return pwd_context.hash(password)
            elif "__about__" in error_msg or "bcrypt" in error_msg.lower():
                # bcrypt互換性エラーの場合、直接bcryptを使用
                import bcrypt

                password_bytes = password.encode("utf-8")
                if len(password_bytes) > 72:
                    password_bytes = password_bytes[:72]
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password_bytes, salt)
                return hashed.decode("utf-8")
            else:
                # その他のエラーは再発生
                raise

    @staticmethod
    def create_access_token(
        data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """アクセストークンの生成"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Dict[str, Any]:
        """アクセストークンのデコード"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """現在のユーザー情報を取得（JWTトークンから）"""
    token = credentials.credentials
    payload = JWTAuth.decode_access_token(token)

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "username": username,
        "email": payload.get("email"),
        "roles": payload.get("roles", []),
        "permissions": payload.get("permissions", []),
    }


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """アクティブなユーザー情報を取得"""
    # ここでユーザーのアクティブ状態をチェック
    # 現在は常にアクティブとして扱う
    return current_user


async def get_current_user_websocket(websocket: WebSocket) -> Optional[Dict[str, Any]]:
    """WebSocket用のユーザー認証"""
    try:
        # クエリパラメータまたはヘッダーからトークンを取得
        token = websocket.query_params.get("token") or websocket.headers.get(
            "Authorization", ""
        ).replace("Bearer ", "")

        if not token:
            return None

        # トークンを検証
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            return None

        # ユーザー情報を返す（簡易実装）
        return {
            "username": username,
            "email": payload.get("email"),
            "is_active": payload.get("is_active", True),
        }
    except JWTError:
        return None
