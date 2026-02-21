"""
GraphQL スキーマ
REST API の一部を GraphQL で提供
"""
import strawberry
from typing import List, Optional


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
class HealthStatus:
    """ヘルスステータス型"""
    status: str
    version: str
    service: str


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
    async def services(self) -> List[Service]:
        """登録サービス一覧"""
        return [
            Service(name="backend-api", url="http://backend:8000", status="active"),
            Service(name="mlops-service", url="http://mlops-service:8003", status="pending"),
            Service(name="generative-ai-service", url="http://generative-ai-service:8004", status="pending"),
            Service(name="security-service", url="http://security-service:8005", status="pending"),
        ]


# スキーマ生成
schema = strawberry.Schema(Query)
