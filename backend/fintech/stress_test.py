"""
金融ストレステスト
規制対応、リスクシナリオ分析
補強スキル: FinTech、規制対応
"""
from dataclasses import dataclass
from datetime import datetime, timezone

from typing import Any, Dict, List


@dataclass
class StressScenario:
    """ストレスシナリオ"""

    name: str
    description: str
    shock_factor: float  # 負のショック係数（例: -0.2 = 20%下落）


def run_stress_test(
    portfolio_value: float,
    scenarios: List[StressScenario],
) -> Dict[str, Any]:
    """
    ストレステストを実行

    Args:
        portfolio_value: ポートフォリオ評価額
        scenarios: シナリオリスト

    Returns:
        シナリオ別の結果
    """
    results = []
    for s in scenarios:
        impact = portfolio_value * s.shock_factor
        results.append(
            {
                "scenario": s.name,
                "description": s.description,
                "original_value": portfolio_value,
                "shock_factor": s.shock_factor,
                "impact": impact,
                "stressed_value": portfolio_value + impact,
            }
        )
    return {
        "portfolio_value": portfolio_value,
        "scenarios": results,
        "max_loss": min(r["impact"] for r in results) if results else 0,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# デフォルトシナリオ
DEFAULT_SCENARIOS = [
    StressScenario("市場急落", "株価20%下落", -0.20),
    StressScenario("金利上昇", "金利2%上昇", -0.15),
    StressScenario("為替変動", "円安10%", -0.05),
]
