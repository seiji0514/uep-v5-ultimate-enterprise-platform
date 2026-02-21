"""
認証・認可APIエンドポイント
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import UserCreate, UserResponse, LoginRequest, TokenResponse, PasswordChangeRequest
from .jwt_auth import JWTAuth, get_current_user, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from .rbac import RBAC
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/auth", tags=["認証"])

# 簡易的なユーザーストレージ（実際の実装ではデータベースを使用）
# デモ用のユーザーデータ（パスワードハッシュは遅延評価）
def _init_demo_users():
    """デモユーザーを初期化（遅延評価）"""
    try:
        return {
            "kaho0525": {
                "username": "kaho0525",
                "email": "kaho0525@example.com",
                "hashed_password": JWTAuth.get_password_hash("kaho052514"),
                "full_name": "管理者",
                "department": "IT",
                "roles": ["admin"],
                "permissions": ["read", "write", "delete", "admin", "manage_users", "manage_roles", "manage_ecosystem"],
                "is_active": True,
                "security_level": 5,
            },
        "developer": {
            "username": "developer",
            "email": "developer@example.com",
            "hashed_password": JWTAuth.get_password_hash("dev123"),
            "full_name": "開発者",
            "department": "開発部",
            "roles": ["developer"],
            "permissions": ["read", "write", "manage_mlops", "manage_ai", "manage_ecosystem"],
            "is_active": True,
            "security_level": 3,
        },
        "viewer": {
            "username": "viewer",
            "email": "viewer@example.com",
            "hashed_password": JWTAuth.get_password_hash("view123"),
            "full_name": "閲覧者",
            "department": "一般",
            "roles": ["viewer"],
            "permissions": ["read"],
            "is_active": True,
            "security_level": 1,
        },
        }
    except Exception as e:
        # 初期化エラー時は空の辞書を返す
        import traceback
        print(f"Error: Failed to initialize demo users: {e}")
        traceback.print_exc()
        return {}

# 遅延初期化（モジュール読み込み時のエラーを防ぐため）
_demo_users_cache: Dict[str, Dict[str, Any]] = {}
_users_initialized = False

def get_demo_users() -> Dict[str, Dict[str, Any]]:
    """デモユーザーを取得（必要時に初期化）"""
    global _demo_users_cache, _users_initialized
    if not _users_initialized:
        try:
            _demo_users_cache = _init_demo_users()
            _users_initialized = True
            import logging
            logging.getLogger(__name__).info(f"Demo users loaded: {list(_demo_users_cache.keys())}")
        except Exception as e:
            # 初期化エラー時は空の辞書を返す
            import traceback
            import logging
            logging.getLogger(__name__).error(f"Failed to initialize demo users: {e}")
            traceback.print_exc()
            _demo_users_cache = {}
    return _demo_users_cache


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """ユーザー登録"""
    users = get_demo_users()
    if user_data.username in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = JWTAuth.get_password_hash(user_data.password)
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "full_name": user_data.full_name,
        "department": user_data.department or "一般",
        "roles": ["user"],
        "permissions": ["read", "write_own"],
        "is_active": True,
        "security_level": 1,
    }

    users[user_data.username] = user

    return UserResponse(
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        department=user["department"],
        roles=user["roles"],
        is_active=user["is_active"],
    )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """ログイン（JWTトークン発行）"""
    users = get_demo_users()
    user = users.get(login_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not JWTAuth.verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    # JWTトークンを生成
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTAuth.create_access_token(
        data={
            "sub": user["username"],
            "email": user["email"],
            "roles": user["roles"],
            "permissions": user["permissions"],
            "department": user["department"],
            "security_level": user["security_level"],
        },
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            department=user["department"],
            roles=user["roles"],
            is_active=user["is_active"],
        )
    )


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2互換のトークンエンドポイント"""
    users = get_demo_users()
    user = users.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not JWTAuth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTAuth.create_access_token(
        data={
            "sub": user["username"],
            "email": user["email"],
            "roles": user["roles"],
            "permissions": user["permissions"],
        },
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            department=user["department"],
            roles=user["roles"],
            is_active=user["is_active"],
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """現在のユーザー情報を取得"""
    users = get_demo_users()
    user = users.get(current_user["username"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        department=user["department"],
        roles=user["roles"],
        permissions=user.get("permissions", []),
        is_active=user["is_active"],
    )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """パスワード変更"""
    users = get_demo_users()
    user = users.get(current_user["username"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not JWTAuth.verify_password(password_data.current_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )

    users = get_demo_users()
    if current_user["username"] in users:
        users[current_user["username"]]["hashed_password"] = JWTAuth.get_password_hash(password_data.new_password)

    return {"message": "Password changed successfully"}
