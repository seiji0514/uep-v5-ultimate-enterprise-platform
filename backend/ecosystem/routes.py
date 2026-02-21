"""
Level 3 エコシステム - APIルート
パートナー統合、コミュニティ機能、業界標準
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .models import (
    ForumComment,
    ForumCommentCreate,
    ForumPost,
    ForumPostCreate,
    MarketplaceItem,
    MarketplaceItemCreate,
    Partner,
    PartnerApproval,
    PartnerCreate,
    Plugin,
    PluginCreate,
    SharedModel,
    SharedModelCreate,
)
from .store import ecosystem_store

router = APIRouter(prefix="/api/v1/ecosystem", tags=["Ecosystem (Level 3)"])


# === パートナー統合 ===
@router.get("/partners", response_model=List[Partner])
@require_permission("read")
async def list_partners(
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """パートナー一覧を取得"""
    return ecosystem_store.list_partners(status=status)


@router.post("/partners", response_model=Partner, status_code=status.HTTP_201_CREATED)
async def register_partner(partner: PartnerCreate):
    """パートナー登録（認証不要・承認プロセス経由）"""
    data = partner.model_dump()
    return ecosystem_store.create_partner(data)


@router.get("/partners/{partner_id}", response_model=Partner)
@require_permission("read")
async def get_partner(
    partner_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """パートナー詳細を取得"""
    p = ecosystem_store.get_partner(partner_id)
    if not p:
        raise HTTPException(status_code=404, detail="Partner not found")
    return p


@router.post("/partners/{partner_id}/approve")
@require_permission("manage_ecosystem")
async def approve_partner(
    partner_id: str,
    approval: PartnerApproval,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """パートナーを承認・却下"""
    p = ecosystem_store.approve_partner(partner_id, approval.approved, approval.notes)
    if not p:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"status": "approved" if approval.approved else "rejected", "partner": p}


# === パートナーマーケットプレイス ===
@router.get("/marketplace", response_model=List[MarketplaceItem])
@require_permission("read")
async def list_marketplace_items(
    category: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """マーケットプレイス一覧を取得"""
    return ecosystem_store.list_marketplace_items(category=category)


@router.post(
    "/marketplace", response_model=MarketplaceItem, status_code=status.HTTP_201_CREATED
)
@require_permission("manage_ecosystem")
async def create_marketplace_item(
    item: MarketplaceItemCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """マーケットプレイスにアイテムを追加"""
    data = item.model_dump()
    return ecosystem_store.create_marketplace_item(data)


@router.get("/marketplace/{item_id}", response_model=MarketplaceItem)
@require_permission("read")
async def get_marketplace_item(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """マーケットプレイスアイテム詳細"""
    item = ecosystem_store.get_marketplace_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Marketplace item not found")
    return item


@router.post("/marketplace/{item_id}/download")
@require_permission("read")
async def download_marketplace_item(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ダウンロード（カウント増加）"""
    ecosystem_store.increment_download(item_id)
    return {"status": "ok", "item_id": item_id}


# === プラグイン ===
@router.get("/plugins", response_model=List[Plugin])
@require_permission("read")
async def list_plugins(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """登録プラグイン一覧"""
    return ecosystem_store.list_plugins()


@router.post("/plugins", response_model=Plugin, status_code=status.HTTP_201_CREATED)
@require_permission("manage_ecosystem")
async def register_plugin(
    plugin: PluginCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """プラグインを登録"""
    return ecosystem_store.create_plugin(plugin.model_dump())


# === モデル共有・配布 ===
@router.get("/shared-models", response_model=List[SharedModel])
@require_permission("read")
async def list_shared_models(
    model_type: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """共有モデル一覧を取得"""
    return ecosystem_store.list_shared_models(model_type=model_type)


@router.post(
    "/shared-models", response_model=SharedModel, status_code=status.HTTP_201_CREATED
)
@require_permission("manage_ecosystem")
async def share_model(
    model: SharedModelCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """モデルを共有"""
    data = model.model_dump()
    data["created_by"] = current_user.get("username", "unknown")
    return ecosystem_store.create_shared_model(data)


@router.post("/shared-models/{model_id}/download")
@require_permission("read")
async def download_shared_model(
    model_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """共有モデルをダウンロード（カウント増加）"""
    if model_id not in ecosystem_store.shared_models:
        raise HTTPException(status_code=404, detail="Shared model not found")
    ecosystem_store.increment_model_download(model_id)
    return {"status": "ok", "model_id": model_id}


# === コミュニティフォーラム ===
@router.get("/forum/posts", response_model=List[ForumPost])
@require_permission("read")
async def list_forum_posts(
    category: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """フォーラム投稿一覧"""
    return ecosystem_store.list_forum_posts(category=category)


@router.post(
    "/forum/posts", response_model=ForumPost, status_code=status.HTTP_201_CREATED
)
@require_permission("read")
async def create_forum_post(
    post: ForumPostCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """フォーラムに投稿"""
    data = post.model_dump()
    data["author"] = current_user.get("username", "anonymous")
    return ecosystem_store.create_forum_post(data)


@router.get("/forum/posts/{post_id}", response_model=ForumPost)
@require_permission("read")
async def get_forum_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """フォーラム投稿詳細"""
    if post_id not in ecosystem_store.forum_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return ecosystem_store.forum_posts[post_id]


@router.get("/forum/posts/{post_id}/comments", response_model=List[ForumComment])
@require_permission("read")
async def list_forum_comments(
    post_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """投稿へのコメント一覧"""
    return ecosystem_store.list_forum_comments(post_id)


@router.post(
    "/forum/posts/{post_id}/comments",
    response_model=ForumComment,
    status_code=status.HTTP_201_CREATED,
)
@require_permission("read")
async def create_forum_comment(
    post_id: str,
    comment: ForumCommentCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """コメントを追加"""
    data = comment.model_dump()
    data["author"] = current_user.get("username", "anonymous")
    result = ecosystem_store.create_forum_comment(post_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return result


# === 業界標準 API 仕様 ===
@router.get("/standard-api-spec")
async def get_standard_api_spec():
    """UEP 標準 API 仕様（OpenAPI 準拠）"""
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "UEP Ecosystem Standard API",
            "version": "1.0.0",
            "description": "UEP v5.0 Level 3 エコシステム標準API仕様。パートナー統合、モデル共有、コミュニティ機能の業界標準。",
        },
        "paths": {
            "/api/v1/ecosystem/partners": {
                "get": {"summary": "パートナー一覧取得"},
                "post": {"summary": "パートナー登録"},
            },
            "/api/v1/ecosystem/marketplace": {
                "get": {"summary": "マーケットプレイス一覧"},
            },
            "/api/v1/ecosystem/shared-models": {
                "get": {"summary": "共有モデル一覧"},
                "post": {"summary": "モデル共有"},
            },
            "/api/v1/ecosystem/forum/posts": {
                "get": {"summary": "フォーラム投稿一覧"},
                "post": {"summary": "投稿作成"},
            },
        },
        "x-uep-level": 3,
        "x-uep-ecosystem": True,
    }


@router.get("/overview")
@require_permission("read")
async def get_ecosystem_overview(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """エコシステム概要（Level 3）"""
    return {
        "level": 3,
        "name": "Ecosystem Level",
        "features": {
            "partner_integration": {
                "description": "サードパーティ統合（API、プラグイン）",
                "partners_count": len(ecosystem_store.partners),
                "marketplace_count": len(ecosystem_store.marketplace_items),
                "plugins_count": len(ecosystem_store.plugins),
            },
            "community": {
                "description": "モデル共有・配布、コミュニティフォーラム",
                "shared_models_count": len(ecosystem_store.shared_models),
                "forum_posts_count": len(ecosystem_store.forum_posts),
            },
            "industry_standard": {
                "description": "標準API仕様の策定",
                "spec_endpoint": "/api/v1/ecosystem/standard-api-spec",
            },
        },
    }
