"""
FinOps - クラウドコスト可視化・予測
補強スキル: FinOps, コスト最適化
"""
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


def get_cost_summary(
    period_days: int = 30,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """
    コストサマリを取得（デモ実装）
    本番では AWS Cost Explorer / GCP Billing API 等と連携
    """
    # デモ用サンプルデータ
    return {
        "period_days": period_days,
        "total_cost_usd": 1250.50,
        "by_service": [
            {"service": "compute", "cost_usd": 650.20, "percentage": 52.0},
            {"service": "storage", "cost_usd": 180.30, "percentage": 14.4},
            {"service": "network", "cost_usd": 95.00, "percentage": 7.6},
            {"service": "database", "cost_usd": 325.00, "percentage": 26.0},
        ],
        "forecast_next_month_usd": 1320.00,
        "recommendations": [
            {
                "type": "rightsizing",
                "description": "idle インスタンスのダウンサイズ推奨",
                "potential_savings_usd": 120,
            },
            {
                "type": "reserved",
                "description": "1年リザーブドで約30%削減可能",
                "potential_savings_usd": 195,
            },
        ],
        "generated_at": datetime.utcnow().isoformat(),
    }


def get_cost_by_tag(tag_key: str, period_days: int = 30) -> List[Dict[str, Any]]:
    """タグ別コスト（デモ）"""
    return [
        {"tag_value": "uep-backend", "cost_usd": 450.00},
        {"tag_value": "uep-mlops", "cost_usd": 320.00},
        {"tag_value": "uep-data", "cost_usd": 480.50},
    ]
