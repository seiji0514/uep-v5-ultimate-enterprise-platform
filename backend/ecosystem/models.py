"""
Level 3 エコシステム - Pydanticモデル
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# === パートナー統合 ===
class PartnerStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class PartnerCreate(BaseModel):
    name: str
    organization: str
    contact_email: str
    description: Optional[str] = None
    api_endpoint: Optional[str] = None


class Partner(BaseModel):
    id: str
    name: str
    organization: str
    contact_email: str
    description: Optional[str] = None
    status: PartnerStatus
    api_endpoint: Optional[str] = None
    created_at: str
    approved_at: Optional[str] = None


class PartnerApproval(BaseModel):
    approved: bool
    notes: Optional[str] = None


# === パートナーマーケットプレイス ===
class MarketplaceItemCreate(BaseModel):
    name: str
    description: str
    category: str  # api, plugin, model, template
    partner_id: str
    price_type: str = "free"  # free, paid
    metadata: Optional[Dict[str, Any]] = None


class MarketplaceItem(BaseModel):
    id: str
    name: str
    description: str
    category: str
    partner_id: str
    partner_name: str
    price_type: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: str
    download_count: int = 0


# === プラグイン ===
class PluginCreate(BaseModel):
    name: str
    version: str
    description: str
    endpoint: str
    partner_id: str
    config_schema: Optional[Dict[str, Any]] = None


class Plugin(BaseModel):
    id: str
    name: str
    version: str
    description: str
    endpoint: str
    partner_id: str
    status: str = "active"
    config_schema: Optional[Dict[str, Any]] = None
    created_at: str


# === モデル共有・配布 ===
class SharedModelCreate(BaseModel):
    model_config = {"protected_namespaces": ()}

    name: str
    description: str
    model_type: str  # ml, llm, embedding
    source: str  # mlops, huggingface, custom
    created_by: str


class SharedModel(BaseModel):
    model_config = {"protected_namespaces": ()}
    id: str
    name: str
    description: str
    model_type: str
    source: str
    created_by: str
    created_at: str
    download_count: int = 0
    tags: List[str] = []


# === コミュニティフォーラム ===
class ForumPostCreate(BaseModel):
    title: str
    content: str
    category: str = "general"  # general, mlops, generative-ai, security, qa


class ForumPost(BaseModel):
    id: str
    title: str
    content: str
    category: str
    author: str
    created_at: str
    comment_count: int = 0
    likes: int = 0


class ForumCommentCreate(BaseModel):
    content: str


class ForumComment(BaseModel):
    id: str
    post_id: str
    content: str
    author: str
    created_at: str
