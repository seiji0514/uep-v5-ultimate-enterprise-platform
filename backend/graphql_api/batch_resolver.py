"""
GraphQL バッチリゾルバ
複数クエリを一括で解決し N+1 を抑制
補強スキル: GraphQL バッチ処理
"""
from typing import Any, Dict, List

from strawberry.dataloader import DataLoader


async def batch_load_users(keys: List[str]) -> List[Dict[str, Any]]:
    """ユーザーをバッチ取得"""
    # 実装例: keys (username) で一括取得
    result = []
    for key in keys:
        result.append(
            {
                "username": key,
                "email": f"{key}@uep.local",
                "full_name": key.capitalize(),
                "department": "Dev",
                "roles": ["user"] if key != "admin" else ["admin"],
                "is_active": True,
            }
        )
    return result


async def batch_load_projects(keys: List[str]) -> List[Dict[str, Any]]:
    """プロジェクトをバッチ取得"""
    result = []
    for key in keys:
        result.append(
            {
                "id": key,
                "name": f"Project {key}",
                "description": "Batch loaded",
                "status": "active",
                "owner_username": "admin",
            }
        )
    return result


def create_batch_loaders() -> Dict[str, DataLoader]:
    """バッチ用 DataLoader を生成"""
    return {
        "user_loader": DataLoader(load_fn=batch_load_users),
        "project_loader": DataLoader(load_fn=batch_load_projects),
    }
