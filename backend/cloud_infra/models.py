"""
クラウドインフラ関連のデータモデル
"""
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ResourceCreate(BaseModel):
    """リソース作成モデル"""

    name: str
    resource_type: str
    provider: str
    region: str
    config: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, str]] = None


class IaCTemplateCreate(BaseModel):
    """IaCテンプレート作成モデル"""

    name: str
    provider: str
    template_content: str
    description: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None


class IaCDeploy(BaseModel):
    """IaCデプロイモデル"""

    variables: Optional[Dict[str, Any]] = None


class DeploymentCreate(BaseModel):
    """デプロイメント作成モデル"""

    name: str
    platform: str
    image: str
    replicas: int = 1
    config: Optional[Dict[str, Any]] = None
    namespace: str = "default"


class DeploymentUpdate(BaseModel):
    """デプロイメント更新モデル"""

    image: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
