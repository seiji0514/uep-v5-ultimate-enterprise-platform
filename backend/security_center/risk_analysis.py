"""
リスク分析モジュール
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RiskLevel(str, Enum):
    """リスクレベル"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Risk(BaseModel):
    """リスク"""

    id: str
    name: str
    description: str
    category: str  # technical, operational, compliance, etc.
    risk_level: RiskLevel
    likelihood: float  # 0.0 - 1.0
    impact: float  # 0.0 - 1.0
    mitigation: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class RiskAnalyzer:
    """リスク分析クラス"""

    def __init__(self):
        """リスク分析器を初期化"""
        self._risks: Dict[str, Risk] = {}
        self._initialize_default_risks()

    def _initialize_default_risks(self):
        """デフォルトリスクを初期化"""
        now = datetime.utcnow()

        default_risks = [
            Risk(
                id=str(uuid.uuid4()),
                name="データ漏洩リスク",
                description="機密データの不正アクセスや漏洩のリスク",
                category="compliance",
                risk_level=RiskLevel.HIGH,
                likelihood=0.3,
                impact=0.9,
                mitigation="暗号化とアクセス制御の強化",
                created_at=now,
                updated_at=now,
            ),
            Risk(
                id=str(uuid.uuid4()),
                name="サービス停止リスク",
                description="システム障害によるサービス停止のリスク",
                category="operational",
                risk_level=RiskLevel.MEDIUM,
                likelihood=0.2,
                impact=0.7,
                mitigation="冗長化と自動フェイルオーバーの実装",
                created_at=now,
                updated_at=now,
            ),
        ]

        for risk in default_risks:
            self._risks[risk.id] = risk

    def calculate_risk_score(self, likelihood: float, impact: float) -> RiskLevel:
        """リスクスコアを計算"""
        score = likelihood * impact

        if score >= 0.7:
            return RiskLevel.CRITICAL
        elif score >= 0.5:
            return RiskLevel.HIGH
        elif score >= 0.3:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def register_risk(
        self,
        name: str,
        description: str,
        category: str,
        likelihood: float,
        impact: float,
        mitigation: Optional[str] = None,
    ) -> Risk:
        """リスクを登録"""
        risk_level = self.calculate_risk_score(likelihood, impact)

        risk = Risk(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            category=category,
            risk_level=risk_level,
            likelihood=likelihood,
            impact=impact,
            mitigation=mitigation,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self._risks[risk.id] = risk
        return risk

    def get_risk(self, risk_id: str) -> Optional[Risk]:
        """リスクを取得"""
        return self._risks.get(risk_id)

    def list_risks(
        self, category: Optional[str] = None, risk_level: Optional[RiskLevel] = None
    ) -> List[Risk]:
        """リスク一覧を取得"""
        risks = list(self._risks.values())

        if category:
            risks = [r for r in risks if r.category == category]

        if risk_level:
            risks = [r for r in risks if r.risk_level == risk_level]

        return sorted(risks, key=lambda r: r.likelihood * r.impact, reverse=True)

    def analyze_security_posture(self) -> Dict[str, Any]:
        """セキュリティ態勢を分析"""
        risks = list(self._risks.values())

        total_risks = len(risks)
        critical_risks = len([r for r in risks if r.risk_level == RiskLevel.CRITICAL])
        high_risks = len([r for r in risks if r.risk_level == RiskLevel.HIGH])

        avg_likelihood = (
            sum(r.likelihood for r in risks) / total_risks if total_risks > 0 else 0
        )
        avg_impact = (
            sum(r.impact for r in risks) / total_risks if total_risks > 0 else 0
        )

        return {
            "total_risks": total_risks,
            "critical_risks": critical_risks,
            "high_risks": high_risks,
            "average_likelihood": avg_likelihood,
            "average_impact": avg_impact,
            "overall_risk_score": avg_likelihood * avg_impact,
            "risk_level": self.calculate_risk_score(avg_likelihood, avg_impact).value,
        }


# グローバルインスタンス
risk_analyzer = RiskAnalyzer()
