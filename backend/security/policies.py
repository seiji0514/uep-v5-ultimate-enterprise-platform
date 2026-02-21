"""
セキュリティポリシー管理モジュール
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SecurityPolicy(BaseModel):
    """セキュリティポリシー"""

    id: str
    name: str
    description: Optional[str] = None
    policy_type: str  # network, access, encryption, etc.
    rules: Dict[str, Any]
    enabled: bool = True
    created_at: datetime
    updated_at: datetime


class SecurityPolicyManager:
    """セキュリティポリシーマネージャークラス"""

    def __init__(self):
        """セキュリティポリシーマネージャーを初期化"""
        self._policies: Dict[str, SecurityPolicy] = {}
        self._initialize_default_policies()

    def _initialize_default_policies(self):
        """デフォルトポリシーを初期化"""
        now = datetime.utcnow()

        default_policies = [
            SecurityPolicy(
                id="default-encryption",
                name="デフォルト暗号化ポリシー",
                description="すべての通信を暗号化",
                policy_type="encryption",
                rules={
                    "require_tls": True,
                    "min_tls_version": "1.2",
                    "require_mtls": False,
                },
                enabled=True,
                created_at=now,
                updated_at=now,
            ),
            SecurityPolicy(
                id="default-rate-limit",
                name="デフォルトレート制限ポリシー",
                description="APIレート制限",
                policy_type="rate_limit",
                rules={"requests_per_minute": 100, "burst_size": 20},
                enabled=True,
                created_at=now,
                updated_at=now,
            ),
            SecurityPolicy(
                id="default-password",
                name="デフォルトパスワードポリシー",
                description="パスワード要件",
                policy_type="password",
                rules={
                    "min_length": 8,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_special_chars": True,
                },
                enabled=True,
                created_at=now,
                updated_at=now,
            ),
        ]

        for policy in default_policies:
            self._policies[policy.id] = policy

    def create_policy(self, policy: SecurityPolicy) -> SecurityPolicy:
        """ポリシーを作成"""
        policy.updated_at = datetime.utcnow()
        self._policies[policy.id] = policy
        return policy

    def get_policy(self, policy_id: str) -> Optional[SecurityPolicy]:
        """ポリシーを取得"""
        return self._policies.get(policy_id)

    def list_policies(
        self, policy_type: Optional[str] = None, enabled_only: bool = False
    ) -> List[SecurityPolicy]:
        """ポリシー一覧を取得"""
        policies = list(self._policies.values())

        if policy_type:
            policies = [p for p in policies if p.policy_type == policy_type]

        if enabled_only:
            policies = [p for p in policies if p.enabled]

        return policies

    def update_policy(self, policy_id: str, **kwargs) -> Optional[SecurityPolicy]:
        """ポリシーを更新"""
        policy = self._policies.get(policy_id)
        if not policy:
            return None

        # 更新可能なフィールドを更新
        update_fields = {"name", "description", "rules", "enabled"}

        for key, value in kwargs.items():
            if key in update_fields:
                setattr(policy, key, value)

        policy.updated_at = datetime.utcnow()
        return policy

    def delete_policy(self, policy_id: str) -> bool:
        """ポリシーを削除"""
        if policy_id in self._policies:
            del self._policies[policy_id]
            return True
        return False

    def get_policy_by_type(self, policy_type: str) -> Optional[SecurityPolicy]:
        """タイプ別にポリシーを取得"""
        for policy in self._policies.values():
            if policy.policy_type == policy_type and policy.enabled:
                return policy
        return None


# グローバルインスタンス
security_policy_manager = SecurityPolicyManager()
