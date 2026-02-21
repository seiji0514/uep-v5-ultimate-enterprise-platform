"""
UEP v5.0 - 認証・認可モジュール
"""
from .jwt_auth import JWTAuth, get_current_user, get_current_active_user
from .oauth2 import OAuth2Provider
from .rbac import RBAC, require_permission, require_role
from .abac import ABAC, check_attribute_access

__all__ = [
    "JWTAuth",
    "get_current_user",
    "get_current_active_user",
    "OAuth2Provider",
    "RBAC",
    "require_permission",
    "require_role",
    "ABAC",
    "check_attribute_access",
]
