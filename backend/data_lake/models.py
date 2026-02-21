"""
データレイク関連のデータモデル
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class BucketCreate(BaseModel):
    """バケット作成モデル"""
    name: str
    region: Optional[str] = None


class BucketResponse(BaseModel):
    """バケットレスポンスモデル"""
    name: str
    creation_date: Optional[str] = None


class ObjectInfo(BaseModel):
    """オブジェクト情報モデル"""
    name: str
    size: int
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None


class CatalogCreate(BaseModel):
    """カタログ作成モデル"""
    model_config = {"protected_namespaces": ()}
    
    name: str
    bucket_name: str
    object_name: str
    data_type: str
    format: str
    description: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class CatalogUpdate(BaseModel):
    """カタログ更新モデル"""
    model_config = {"protected_namespaces": ()}
    
    name: Optional[str] = None
    description: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class GovernancePolicyCreate(BaseModel):
    """ガバナンスポリシー作成モデル"""
    id: str
    name: str
    description: Optional[str] = None
    bucket_pattern: str
    object_pattern: Optional[str] = None
    retention_policy: str
    access_level: str
    allowed_roles: Optional[List[str]] = None
    encryption_required: bool = False
    audit_enabled: bool = True
