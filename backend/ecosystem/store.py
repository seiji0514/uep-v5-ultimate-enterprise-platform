"""
Level 3 エコシステム - インメモリストア
"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid
from .models import PartnerStatus


class EcosystemStore:
    """エコシステムデータのインメモリストア"""

    def __init__(self):
        self.partners: Dict[str, dict] = {}
        self.marketplace_items: Dict[str, dict] = {}
        self.plugins: Dict[str, dict] = {}
        self.shared_models: Dict[str, dict] = {}
        self.forum_posts: Dict[str, dict] = {}
        self.forum_comments: Dict[str, dict] = {}
        self._init_demo_data()

    def _init_demo_data(self):
        """デモ用初期データ"""
        # デモパートナー
        p1 = {
            "id": "partner-001",
            "name": "AI Solutions Inc.",
            "organization": "AI Solutions Inc.",
            "contact_email": "partner@aisolutions.example.com",
            "description": "ML/AI ソリューション提供",
            "status": PartnerStatus.APPROVED.value,
            "api_endpoint": "https://api.aisolutions.example.com",
            "created_at": datetime.utcnow().isoformat(),
            "approved_at": datetime.utcnow().isoformat(),
        }
        self.partners[p1["id"]] = p1

        # デモマーケットプレイス
        m1 = {
            "id": "mp-001",
            "name": "UEP RAG テンプレート",
            "description": "RAG パターン実装用テンプレート",
            "category": "template",
            "partner_id": "partner-001",
            "partner_name": "AI Solutions Inc.",
            "price_type": "free",
            "metadata": {"version": "1.0", "tags": ["rag", "llm"]},
            "created_at": datetime.utcnow().isoformat(),
            "download_count": 42,
        }
        self.marketplace_items[m1["id"]] = m1

        # デモ共有モデル
        sm1 = {
            "id": "model-001",
            "name": "UEP-Sentiment-v1",
            "description": "感情分析用ファインチューニングモデル",
            "model_type": "ml",
            "source": "mlops",
            "created_by": "kaho0525",
            "created_at": datetime.utcnow().isoformat(),
            "download_count": 15,
            "tags": ["sentiment", "nlp"],
        }
        self.shared_models[sm1["id"]] = sm1

        # デモフォーラム投稿
        fp1 = {
            "id": "post-001",
            "title": "UEP v5.0 Level 3 エコシステムの使い方",
            "content": "Level 3 エコシステムでは、パートナー統合、モデル共有、コミュニティフォーラムを利用できます。",
            "category": "general",
            "author": "kaho0525",
            "created_at": datetime.utcnow().isoformat(),
            "comment_count": 2,
            "likes": 5,
        }
        self.forum_posts[fp1["id"]] = fp1

        fc1 = {
            "id": "comment-001",
            "post_id": "post-001",
            "content": "素晴らしい機能ですね！",
            "author": "user1",
            "created_at": datetime.utcnow().isoformat(),
        }
        self.forum_comments[fc1["id"]] = fc1

    # === パートナー ===
    def create_partner(self, data: dict) -> dict:
        pid = f"partner-{uuid.uuid4().hex[:8]}"
        data["id"] = pid
        data["status"] = PartnerStatus.PENDING.value
        data["created_at"] = datetime.utcnow().isoformat()
        data["approved_at"] = None
        self.partners[pid] = data
        return data

    def get_partner(self, partner_id: str) -> Optional[dict]:
        return self.partners.get(partner_id)

    def list_partners(self, status: Optional[str] = None) -> List[dict]:
        items = list(self.partners.values())
        if status:
            items = [p for p in items if p["status"] == status]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

    def approve_partner(self, partner_id: str, approved: bool, notes: Optional[str] = None) -> Optional[dict]:
        p = self.partners.get(partner_id)
        if not p:
            return None
        p["status"] = PartnerStatus.APPROVED.value if approved else PartnerStatus.REJECTED.value
        p["approved_at"] = datetime.utcnow().isoformat() if approved else None
        if notes:
            p["approval_notes"] = notes
        return p

    # === マーケットプレイス ===
    def create_marketplace_item(self, data: dict) -> dict:
        mid = f"mp-{uuid.uuid4().hex[:8]}"
        partner = self.partners.get(data["partner_id"])
        data["id"] = mid
        data["partner_name"] = partner["name"] if partner else "Unknown"
        data["created_at"] = datetime.utcnow().isoformat()
        data["download_count"] = 0
        self.marketplace_items[mid] = data
        return data

    def list_marketplace_items(self, category: Optional[str] = None) -> List[dict]:
        items = list(self.marketplace_items.values())
        if category:
            items = [i for i in items if i["category"] == category]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

    def get_marketplace_item(self, item_id: str) -> Optional[dict]:
        return self.marketplace_items.get(item_id)

    def increment_download(self, item_id: str):
        if item_id in self.marketplace_items:
            self.marketplace_items[item_id]["download_count"] += 1

    # === プラグイン ===
    def create_plugin(self, data: dict) -> dict:
        plid = f"plugin-{uuid.uuid4().hex[:8]}"
        data["id"] = plid
        data["status"] = "active"
        data["created_at"] = datetime.utcnow().isoformat()
        self.plugins[plid] = data
        return data

    def list_plugins(self) -> List[dict]:
        return list(self.plugins.values())

    # === 共有モデル ===
    def create_shared_model(self, data: dict) -> dict:
        mid = f"model-{uuid.uuid4().hex[:8]}"
        data["id"] = mid
        data["created_at"] = datetime.utcnow().isoformat()
        data.setdefault("download_count", 0)
        data.setdefault("tags", [])
        self.shared_models[mid] = data
        return data

    def list_shared_models(self, model_type: Optional[str] = None) -> List[dict]:
        items = list(self.shared_models.values())
        if model_type:
            items = [m for m in items if m["model_type"] == model_type]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

    def increment_model_download(self, model_id: str):
        if model_id in self.shared_models:
            self.shared_models[model_id]["download_count"] += 1

    # === フォーラム ===
    def create_forum_post(self, data: dict) -> dict:
        pid = f"post-{uuid.uuid4().hex[:8]}"
        data["id"] = pid
        data["created_at"] = datetime.utcnow().isoformat()
        data["comment_count"] = 0
        data["likes"] = 0
        self.forum_posts[pid] = data
        return data

    def list_forum_posts(self, category: Optional[str] = None) -> List[dict]:
        items = list(self.forum_posts.values())
        if category:
            items = [p for p in items if p["category"] == category]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

    def create_forum_comment(self, post_id: str, data: dict) -> Optional[dict]:
        if post_id not in self.forum_posts:
            return None
        cid = f"comment-{uuid.uuid4().hex[:8]}"
        data["id"] = cid
        data["post_id"] = post_id
        data["created_at"] = datetime.utcnow().isoformat()
        self.forum_comments[cid] = data
        self.forum_posts[post_id]["comment_count"] += 1
        return data

    def list_forum_comments(self, post_id: str) -> List[dict]:
        return [c for c in self.forum_comments.values() if c["post_id"] == post_id]


ecosystem_store = EcosystemStore()
