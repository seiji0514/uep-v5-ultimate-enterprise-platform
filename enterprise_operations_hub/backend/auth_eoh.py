"""認証・RBAC（Enterprise Operations Hub 用）"""
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

SECRET_KEY = os.getenv("EOH_SECRET_KEY", "eoh-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def validate_production() -> None:
    """本番環境時の必須設定チェック"""
    env = os.environ.get("ENVIRONMENT", "development").lower()
    if env != "production":
        return
    if not SECRET_KEY or SECRET_KEY in ("eoh-secret-key-change-in-production", "change-in-production"):
        raise ValueError(
            "本番環境では EOH_SECRET_KEY を必ず設定してください。"
            "例: EOH_SECRET_KEY=$(openssl rand -hex 32)"
        )

# デモユーザー（DB未使用時）
DEMO_USERS = {
    "kaho0525": {
        "username": "kaho0525",
        "hashed_password": pwd_context.hash("0525"),
        "full_name": "管理者",
        "role": "admin",
        "permissions": ["read", "write", "delete", "admin", "export", "manage_alerts"],
    },
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "full_name": "管理者",
        "role": "admin",
        "permissions": ["read", "write", "delete", "admin", "export", "manage_alerts"],
    },
    "operator": {
        "username": "operator",
        "hashed_password": pwd_context.hash("op123"),
        "full_name": "オペレーター",
        "role": "operator",
        "permissions": ["read", "write", "export", "manage_alerts"],
    },
    "viewer": {
        "username": "viewer",
        "hashed_password": pwd_context.hash("view123"),
        "full_name": "閲覧者",
        "role": "viewer",
        "permissions": ["read", "export"],
    },
}


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    return DEMO_USERS.get(username)


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return {**user, "sub": username}


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {**user, "sub": username}


def require_permission(permission: str):
    async def _check(user: Dict[str, Any] = Depends(get_current_user)):
        perms = user.get("permissions", [])
        if "admin" in perms or permission in perms:
            return user
        raise HTTPException(status_code=403, detail=f"Permission '{permission}' required")
    return _check


OptionalAuth = Depends(security)
