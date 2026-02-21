"""
GraphQL ルーター
FastAPI への GraphQL エンドポイント登録
"""
from strawberry.fastapi import GraphQLRouter
from .schema import schema

# GraphQL ルーター（app.include_router で prefix="/graphql" としてマウント）
graphql_router = GraphQLRouter(
    schema,
    path="/",
    graphql_ide="graphiql",  # 開発用 GraphiQL IDE
    allow_queries_via_get=True,
)
