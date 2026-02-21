"""
ゼロトラストアーキテクチャモジュール
すべての通信を検証・認証
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel


class TrustLevel(str, Enum):
    """信頼レベル"""
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"


class ZeroTrustPolicyModel(BaseModel):
    """ゼロトラストポリシーモデル"""
    id: str
    name: str
    description: Optional[str] = None
    resource_pattern: str  # リソースパターン
    required_trust_level: TrustLevel
    required_roles: List[str] = []
    required_permissions: List[str] = []
    ip_whitelist: Optional[List[str]] = None
    ip_blacklist: Optional[List[str]] = None
    time_restrictions: Optional[Dict[str, Any]] = None
    mfa_required: bool = False
    created_at: datetime
    updated_at: datetime


class ZeroTrustPolicy:
    """ゼロトラストポリシークラス"""

    def __init__(self):
        """ゼロトラストポリシーを初期化"""
        self._policies: Dict[str, ZeroTrustPolicyModel] = {}
        self._initialize_default_policies()

    def _initialize_default_policies(self):
        """デフォルトポリシーを初期化"""
        now = datetime.utcnow()

        default_policies = [
            ZeroTrustPolicyModel(
                id="default-admin",
                name="管理者アクセスポリシー",
                description="管理者リソースへのアクセス",
                resource_pattern="/api/v1/admin/*",
                required_trust_level=TrustLevel.VERIFIED,
                required_roles=["admin"],
                mfa_required=True,
                created_at=now,
                updated_at=now
            ),
            ZeroTrustPolicyModel(
                id="default-api",
                name="APIアクセスポリシー",
                description="一般APIへのアクセス",
                resource_pattern="/api/v1/*",
                required_trust_level=TrustLevel.MEDIUM,
                required_permissions=["read"],
                created_at=now,
                updated_at=now
            ),
            ZeroTrustPolicyModel(
                id="default-security",
                name="セキュリティリソースポリシー",
                description="セキュリティ関連リソースへのアクセス",
                resource_pattern="/api/v1/security/*",
                required_trust_level=TrustLevel.HIGH,
                required_roles=["admin", "security"],
                mfa_required=True,
                created_at=now,
                updated_at=now
            ),
        ]

        for policy in default_policies:
            self._policies[policy.id] = policy

    def evaluate_access(
        self,
        resource_path: str,
        user_attributes: Dict[str, Any],
        request_attributes: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        アクセスを評価

        Args:
            resource_path: リソースパス
            user_attributes: ユーザー属性（roles, permissions等）
            request_attributes: リクエスト属性（ip, timestamp等）

        Returns:
            (許可されるかどうか, 理由)
        """
        # 適用可能なポリシーを検索
        applicable_policy = self._find_applicable_policy(resource_path)
        if not applicable_policy:
            # ポリシーがない場合はデフォルトで拒否（ゼロトラスト）
            return False, "No policy found, access denied by default"

        # 信頼レベルのチェック
        user_trust_level = self._calculate_user_trust_level(user_attributes)
        if self._compare_trust_levels(user_trust_level, applicable_policy.required_trust_level) < 0:
            return False, f"Insufficient trust level. Required: {applicable_policy.required_trust_level}"

        # ロールチェック
        if applicable_policy.required_roles:
            user_roles = user_attributes.get("roles", [])
            if not any(role in applicable_policy.required_roles for role in user_roles):
                return False, f"Required roles: {applicable_policy.required_roles}"

        # パーミッションチェック
        if applicable_policy.required_permissions:
            user_permissions = user_attributes.get("permissions", [])
            if not any(perm in applicable_policy.required_permissions for perm in user_permissions):
                return False, f"Required permissions: {applicable_policy.required_permissions}"

        # IPチェック
        client_ip = request_attributes.get("ip")
        if client_ip:
            if applicable_policy.ip_blacklist and client_ip in applicable_policy.ip_blacklist:
                return False, "IP address is blacklisted"

            if applicable_policy.ip_whitelist and client_ip not in applicable_policy.ip_whitelist:
                return False, "IP address is not whitelisted"

        # MFAチェック
        if applicable_policy.mfa_required:
            mfa_verified = user_attributes.get("mfa_verified", False)
            if not mfa_verified:
                return False, "MFA verification required"

        return True, None

    def _find_applicable_policy(self, resource_path: str) -> Optional[ZeroTrustPolicyModel]:
        """適用可能なポリシーを検索"""
        for policy in self._policies.values():
            if self._match_pattern(resource_path, policy.resource_pattern):
                return policy
        return None

    def _match_pattern(self, path: str, pattern: str) -> bool:
        """パターンマッチング"""
        import fnmatch
        return fnmatch.fnmatch(path, pattern)

    def _calculate_user_trust_level(self, user_attributes: Dict[str, Any]) -> TrustLevel:
        """ユーザーの信頼レベルを計算"""
        # 簡易的な実装
        if user_attributes.get("mfa_verified"):
            return TrustLevel.VERIFIED
        elif user_attributes.get("roles") and "admin" in user_attributes.get("roles", []):
            return TrustLevel.HIGH
        elif user_attributes.get("roles"):
            return TrustLevel.MEDIUM
        else:
            return TrustLevel.LOW

    def _compare_trust_levels(self, level1: TrustLevel, level2: TrustLevel) -> int:
        """信頼レベルを比較"""
        levels = {
            TrustLevel.UNTRUSTED: 0,
            TrustLevel.LOW: 1,
            TrustLevel.MEDIUM: 2,
            TrustLevel.HIGH: 3,
            TrustLevel.VERIFIED: 4,
        }
        return levels.get(level1, 0) - levels.get(level2, 0)


# グローバルインスタンス
zero_trust_policy = ZeroTrustPolicy()
