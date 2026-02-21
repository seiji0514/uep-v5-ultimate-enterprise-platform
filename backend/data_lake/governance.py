"""
データガバナンスモジュール
データのライフサイクル管理、アクセス制御
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RetentionPolicy(str, Enum):
    """保持ポリシー"""

    IMMEDIATE = "immediate"  # 即座に削除
    DAYS_7 = "7days"
    DAYS_30 = "30days"
    DAYS_90 = "90days"
    DAYS_365 = "365days"
    PERMANENT = "permanent"  # 永続保持


class AccessLevel(str, Enum):
    """アクセスレベル"""

    PUBLIC = "public"  # 全員アクセス可能
    INTERNAL = "internal"  # 内部のみ
    RESTRICTED = "restricted"  # 制限付き
    PRIVATE = "private"  # プライベート


class DataGovernancePolicy(BaseModel):
    """データガバナンスポリシー"""

    id: str
    name: str
    description: Optional[str] = None
    bucket_pattern: str  # バケット名のパターン（ワイルドカード対応）
    object_pattern: Optional[str] = None  # オブジェクト名のパターン
    retention_policy: RetentionPolicy
    access_level: AccessLevel
    allowed_roles: List[str] = []
    encryption_required: bool = False
    audit_enabled: bool = True
    created_at: datetime
    updated_at: datetime


class DataGovernance:
    """データガバナンスクラス"""

    def __init__(self):
        """データガバナンスを初期化"""
        # 簡易的なインメモリストレージ（実際の実装ではデータベースを使用）
        self._policies: Dict[str, DataGovernancePolicy] = {}

        # デフォルトポリシーを追加
        self._initialize_default_policies()

    def _initialize_default_policies(self):
        """デフォルトポリシーを初期化"""
        now = datetime.utcnow()

        default_policies = [
            DataGovernancePolicy(
                id="default-raw-data",
                name="生データポリシー",
                description="生データのデフォルトポリシー",
                bucket_pattern="raw-data*",
                retention_policy=RetentionPolicy.DAYS_365,
                access_level=AccessLevel.RESTRICTED,
                allowed_roles=["admin", "developer"],
                encryption_required=True,
                created_at=now,
                updated_at=now,
            ),
            DataGovernancePolicy(
                id="default-processed-data",
                name="処理済みデータポリシー",
                description="処理済みデータのデフォルトポリシー",
                bucket_pattern="processed-data*",
                retention_policy=RetentionPolicy.DAYS_90,
                access_level=AccessLevel.INTERNAL,
                allowed_roles=["admin", "developer", "operator"],
                created_at=now,
                updated_at=now,
            ),
            DataGovernancePolicy(
                id="default-ml-models",
                name="MLモデルポリシー",
                description="MLモデルのデフォルトポリシー",
                bucket_pattern="ml-models*",
                retention_policy=RetentionPolicy.PERMANENT,
                access_level=AccessLevel.RESTRICTED,
                allowed_roles=["admin", "developer"],
                encryption_required=True,
                created_at=now,
                updated_at=now,
            ),
        ]

        for policy in default_policies:
            self._policies[policy.id] = policy

    def create_policy(self, policy: DataGovernancePolicy) -> DataGovernancePolicy:
        """ポリシーを作成"""
        self._policies[policy.id] = policy
        return policy

    def get_policy(self, policy_id: str) -> Optional[DataGovernancePolicy]:
        """ポリシーを取得"""
        return self._policies.get(policy_id)

    def list_policies(self) -> List[DataGovernancePolicy]:
        """ポリシー一覧を取得"""
        return list(self._policies.values())

    def find_policy_for_bucket(
        self, bucket_name: str
    ) -> Optional[DataGovernancePolicy]:
        """バケットに適用されるポリシーを検索"""
        for policy in self._policies.values():
            if self._match_pattern(bucket_name, policy.bucket_pattern):
                return policy
        return None

    def _match_pattern(self, text: str, pattern: str) -> bool:
        """パターンマッチング（簡易実装）"""
        if "*" in pattern:
            prefix = pattern.split("*")[0]
            return text.startswith(prefix)
        return text == pattern

    def check_access(
        self,
        bucket_name: str,
        user_roles: List[str],
        required_level: Optional[AccessLevel] = None,
    ) -> bool:
        """アクセス権限をチェック"""
        policy = self.find_policy_for_bucket(bucket_name)
        if not policy:
            # ポリシーがない場合はデフォルトで許可
            return True

        # アクセスレベルチェック
        if required_level:
            access_levels = {
                AccessLevel.PUBLIC: 0,
                AccessLevel.INTERNAL: 1,
                AccessLevel.RESTRICTED: 2,
                AccessLevel.PRIVATE: 3,
            }
            if access_levels[policy.access_level] > access_levels[required_level]:
                return False

        # ロールチェック
        if policy.allowed_roles:
            return any(role in policy.allowed_roles for role in user_roles)

        return True

    def get_retention_date(
        self, bucket_name: str, created_date: datetime
    ) -> Optional[datetime]:
        """保持期限日を取得"""
        policy = self.find_policy_for_bucket(bucket_name)
        if not policy or policy.retention_policy == RetentionPolicy.PERMANENT:
            return None

        retention_days = {
            RetentionPolicy.IMMEDIATE: 0,
            RetentionPolicy.DAYS_7: 7,
            RetentionPolicy.DAYS_30: 30,
            RetentionPolicy.DAYS_90: 90,
            RetentionPolicy.DAYS_365: 365,
        }

        days = retention_days.get(policy.retention_policy)
        if days is None:
            return None

        return created_date + timedelta(days=days)


# グローバルインスタンス
governance = DataGovernance()
