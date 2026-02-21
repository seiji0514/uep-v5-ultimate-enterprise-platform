"""
セキュリティ関連のデータモデル
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class SecretCreate(BaseModel):
    """シークレット作成モデル"""
    data: Dict[str, Any]


class SecretResponse(BaseModel):
    """シークレットレスポンスモデル"""
    path: str
    name: str


class PolicyCreate(BaseModel):
    """ポリシー作成モデル"""
    id: str
    name: str
    description: Optional[str] = None
    policy_type: str
    rules: Dict[str, Any]
    enabled: bool = True


class PolicyUpdate(BaseModel):
    """ポリシー更新モデル"""
    name: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None
