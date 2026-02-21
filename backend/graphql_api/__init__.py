"""GraphQL API モジュール（graphql パッケージとの名前衝突を避けるため graphql_api）"""
from .schema import schema

__all__ = ["schema"]
