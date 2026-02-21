"""
Level 2 プラットフォーム - 設計・設定
マルチテナント、SaaS化、セルフサービスプロビジョニング
"""

# セルフサービスプロビジョニング設計
SELF_SERVICE_CONFIG = {
    "enabled": True,
    "tenant_provisioning": {
        "auto_approval": True,
        "default_plan": "starter",
        "trial_days": 14,
    },
    "resource_provisioning": {
        "auto_scaling": True,
        "min_replicas": 1,
        "max_replicas": 10,
    },
}

# マルチテナント分離設計
MULTI_TENANT_CONFIG = {
    "isolation_mode": "schema_per_tenant",
    "data_isolation": True,
    "resource_quota_enforcement": True,
}
