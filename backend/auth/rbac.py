"""
RBAC（ロールベースアクセス制御）モジュール
ロールとパーミッションに基づくアクセス制御
"""
from typing import List, Set, Optional, Dict, Callable
from functools import wraps
from fastapi import HTTPException, status, Depends
from .jwt_auth import get_current_user
import inspect


class RBAC:
    """RBAC（ロールベースアクセス制御）クラス"""

    # ロールとパーミッションのマッピング
    ROLE_PERMISSIONS: Dict[str, Set[str]] = {
        "admin": {
            "read", "write", "delete", "admin", "manage_users", "manage_roles", "manage_ecosystem"
        },
        "developer": {
            "read", "write", "manage_mlops", "manage_ai", "manage_ecosystem"
        },
        "operator": {
            "read", "write", "monitor", "manage_infrastructure", "manage_ecosystem"
        },
        "viewer": {
            "read"
        },
        "user": {
            "read", "write_own"
        }
    }

    @classmethod
    def get_permissions_for_role(cls, role: str) -> Set[str]:
        """ロールに紐づくパーミッションを取得"""
        return cls.ROLE_PERMISSIONS.get(role, set())

    @classmethod
    def get_permissions_for_roles(cls, roles: List[str]) -> Set[str]:
        """複数のロールに紐づくパーミッションを取得（和集合）"""
        permissions = set()
        for role in roles:
            permissions.update(cls.get_permissions_for_role(role))
        return permissions

    @classmethod
    def has_permission(cls, user_permissions: Set[str], required_permission: str) -> bool:
        """ユーザーが指定されたパーミッションを持っているか確認"""
        return required_permission in user_permissions

    @classmethod
    def has_role(cls, user_roles: List[str], required_role: str) -> bool:
        """ユーザーが指定されたロールを持っているか確認"""
        return required_role in user_roles


def require_permission(permission: str):
    """パーミッションチェックデコレータ（FastAPI互換）"""
    def decorator(func: Callable):
        # 元の関数のシグネチャを保持
        sig = inspect.signature(func)
        
        # 新しいシグネチャを作成（current_userパラメータを保持）
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 関数のパラメータをバインド
            try:
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
            except TypeError:
                # パラメータのバインドに失敗した場合、そのまま実行
                return await func(*args, **kwargs)
            
            # current_userを取得
            if 'current_user' not in bound.arguments:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="current_user parameter not found in function signature"
                )
            
            current_user = bound.arguments['current_user']
            user_permissions = set(current_user.get("permissions", []))

            if not RBAC.has_permission(user_permissions, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{permission}' required"
                )

            # パラメータを正しく渡す
            return await func(*args, **kwargs)
        
        # 関数のシグネチャを更新（FastAPIが認識できるように）
        wrapper.__signature__ = sig
        return wrapper
    return decorator


def require_role(role: str):
    """ロールチェックデコレータ（FastAPI互換）"""
    def decorator(func: Callable):
        # 元の関数のシグネチャを保持
        sig = inspect.signature(func)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 関数のパラメータをバインド
            try:
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
            except TypeError:
                # パラメータのバインドに失敗した場合、そのまま実行
                return await func(*args, **kwargs)
            
            # current_userを取得
            if 'current_user' not in bound.arguments:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="current_user parameter not found in function signature"
                )
            
            current_user = bound.arguments['current_user']
            user_roles = current_user.get("roles", [])

            if not RBAC.has_role(user_roles, role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role '{role}' required"
                )

            # パラメータを正しく渡す
            return await func(*args, **kwargs)
        
        # 関数のシグネチャを更新（FastAPIが認識できるように）
        wrapper.__signature__ = sig
        return wrapper
    return decorator
