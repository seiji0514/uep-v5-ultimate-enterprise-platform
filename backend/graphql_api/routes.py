"""
GraphQL ルーター
FastAPI への GraphQL エンドポイント登録
補強スキル: GraphQL（DataLoaderでN+1対策、バッチリゾルバ、キャッシュ）
"""
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter

from .batch_resolver import create_batch_loaders
from .schema import batch_load_services, schema


async def get_context():
    """リクエストごとのコンテキスト（DataLoaderはリクエスト単位で生成）"""
    ctx = {"service_loader": DataLoader(load_fn=batch_load_services)}
    ctx.update(create_batch_loaders())
    return ctx


# GraphQL ルーター（app.include_router で prefix="/graphql" としてマウント）
graphql_router = GraphQLRouter(
    schema,
    path="/",
    graphql_ide="graphiql",  # 開発用 GraphiQL IDE
    allow_queries_via_get=True,
    context_getter=get_context,
)
