"""
GraphQL スキーマ
REST API の一部を GraphQL で提供
補強スキル: GraphQL（DataLoader、サブスクリプション、フェデレーション）
"""
import asyncio
from typing import AsyncGenerator, List, Optional

import strawberry
from strawberry.dataloader import DataLoader
from strawberry.types import Info


@strawberry.type
class User:
    """ユーザー型"""

    username: str
    email: str
    full_name: Optional[str] = None
    department: Optional[str] = None
    roles: List[str]
    is_active: bool = True


@strawberry.type
class Service:
    """サービス型"""

    name: str
    url: str
    status: str


@strawberry.type
class ServiceDetail:
    """サービス詳細（DataLoaderでバッチ取得）"""

    name: str
    url: str
    status: str
    endpoint_count: int


async def batch_load_services(keys: List[str]) -> List[ServiceDetail]:
    """DataLoader: 複数サービスの詳細をバッチ取得（N+1対策）"""
    # 実装例: keys で一括取得し、順序を保持して返す
    result = []
    for key in keys:
        result.append(
            ServiceDetail(
                name=key,
                url=f"http://{key}:8000",
                status="active",
                endpoint_count=5,
            )
        )
    return result


@strawberry.type
class HealthStatus:
    """ヘルスステータス型"""

    status: str
    version: str
    service: str


@strawberry.type
class Project:
    """プロジェクト型（スキーマ拡張）"""

    id: str
    name: str
    description: Optional[str] = None
    status: str = "active"
    owner_username: Optional[str] = None


@strawberry.type
class Query:
    """GraphQL クエリ"""

    @strawberry.field
    async def hello(self) -> str:
        """挨拶"""
        return "Hello from UEP v5.0 GraphQL!"

    @strawberry.field
    async def health(self) -> HealthStatus:
        """ヘルスチェック情報"""
        return HealthStatus(
            status="healthy",
            version="5.0.0",
            service="UEP v5.0 Backend API",
        )

    @strawberry.field
    async def service_detail(
        self, info: Info, name: str
    ) -> Optional[ServiceDetail]:
        """サービス詳細（DataLoader経由・N+1対策）"""
        loader = info.context["service_loader"]
        return await loader.load(name)

    @strawberry.field
    async def services(self) -> List[Service]:
        """登録サービス一覧"""
        return [
            Service(name="backend-api", url="http://backend:8000", status="active"),
            Service(
                name="mlops-service", url="http://mlops-service:8003", status="pending"
            ),
            Service(
                name="generative-ai-service",
                url="http://generative-ai-service:8004",
                status="pending",
            ),
            Service(
                name="security-service",
                url="http://security-service:8005",
                status="pending",
            ),
        ]

    @strawberry.field
    async def projects(self) -> List[Project]:
        """プロジェクト一覧"""
        return [
            Project(id="p1", name="UEP Core", description="基盤システム", owner_username="admin"),
            Project(id="p2", name="MLOps", description="ML運用", status="active"),
        ]

    @strawberry.field
    async def users(self) -> List[User]:
        """ユーザー一覧（サンプル）"""
        return [
            User(username="admin", email="admin@uep.local", roles=["admin"], full_name="管理者"),
            User(username="user1", email="user1@uep.local", roles=["user"], department="Dev"),
        ]


@strawberry.type
class Subscription:
    """GraphQL サブスクリプション（WebSocket リアルタイム）"""

    @strawberry.subscription
    async def health_updates(self, interval_sec: float = 2.0) -> AsyncGenerator[HealthStatus, None]:
        """ヘルスステータスの定期配信（デモ）"""
        for _ in range(5):
            yield HealthStatus(
                status="healthy",
                version="5.0.0",
                service="UEP v5.0 Backend API",
            )
            await asyncio.sleep(interval_sec)

    @strawberry.subscription
    async def service_status(self) -> AsyncGenerator[Service, None]:
        """サービスステータス変更のシミュレーション"""
        services = [
            Service("backend-api", "http://backend:8000", "active"),
            Service("mlops-service", "http://mlops:8003", "pending"),
        ]
        for svc in services:
            yield svc
            await asyncio.sleep(1.0)


# スキーマ生成（Query + Subscription）
schema = strawberry.Schema(query=Query, subscription=Subscription)
