"""
認証・認可関連のデータモデル
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    """ユーザー作成モデル"""

    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    department: Optional[str] = None


class UserResponse(BaseModel):
    """ユーザーレスポンスモデル"""

    username: str
    email: str
    full_name: Optional[str] = None
    department: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []  # 契約: /me で必須
    is_active: bool = True
    created_at: Optional[datetime] = None


class LoginRequest(BaseModel):
    """ログインリクエストモデル"""

    username: str
    password: str

    @field_validator("username", "password", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        """前後の空白を除去"""
        return (v or "").strip()


class TokenResponse(BaseModel):
    """トークンレスポンスモデル"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordChangeRequest(BaseModel):
    """パスワード変更リクエストモデル"""

    current_password: str
    new_password: str
