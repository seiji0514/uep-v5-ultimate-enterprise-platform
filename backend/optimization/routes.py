"""
最適化APIエンドポイント
異常検知（閾値調整・アンサンブル）、設定管理
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.jwt_auth import get_current_active_user


class BatchAnomalyRequest(BaseModel):
    """バッチ異常検知リクエスト"""

    domain: str = "manufacturing"
    items: List[Dict[str, Any]] = []


from core.anomaly_detector import (
    DEFAULT_THRESHOLDS,
    ThresholdConfig,
    ensemble_detect,
    get_anomaly_list,
)
from optimization.finops import get_cost_by_tag, get_cost_summary

router = APIRouter(prefix="/api/v1/optimization", tags=["最適化"])

# メモリ上で閾値オーバーライドを保持（本番ではDB等に永続化）
_threshold_overrides: Dict[str, Dict[str, float]] = {}


def _get_threshold_config(metric: str) -> ThresholdConfig:
    """閾値設定を取得（オーバーライド対応）"""
    base = DEFAULT_THRESHOLDS.get(metric, ThresholdConfig(metric, 999, -999))
    over = _threshold_overrides.get(metric)
    if over:
        return ThresholdConfig(
            metric=base.metric,
            upper=over.get("upper", base.upper),
            lower=over.get("lower", base.lower),
            severity_high_ratio=over.get(
                "severity_high_ratio", base.severity_high_ratio
            ),
            severity_medium_ratio=over.get(
                "severity_medium_ratio", base.severity_medium_ratio
            ),
        )
    return base


@router.get("/anomaly-detection/thresholds")
async def get_thresholds(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """現在の閾値設定一覧を取得"""
    configs = {}
    for k, v in DEFAULT_THRESHOLDS.items():
        c = _get_threshold_config(k)
        configs[k] = {
            "metric": c.metric,
            "upper": c.upper,
            "lower": c.lower,
            "severity_high_ratio": c.severity_high_ratio,
            "severity_medium_ratio": c.severity_medium_ratio,
        }
    return {"thresholds": configs}


@router.put("/anomaly-detection/thresholds/{metric}")
async def update_threshold(
    metric: str,
    upper: Optional[float] = None,
    lower: Optional[float] = None,
    severity_high_ratio: Optional[float] = None,
    severity_medium_ratio: Optional[float] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """閾値を調整"""
    if metric not in _threshold_overrides:
        base = DEFAULT_THRESHOLDS.get(metric, ThresholdConfig(metric, 999, -999))
        _threshold_overrides[metric] = {
            "upper": base.upper,
            "lower": base.lower,
            "severity_high_ratio": base.severity_high_ratio,
            "severity_medium_ratio": base.severity_medium_ratio,
        }
    over = _threshold_overrides[metric]
    if upper is not None:
        over["upper"] = upper
    if lower is not None:
        over["lower"] = lower
    if severity_high_ratio is not None:
        over["severity_high_ratio"] = severity_high_ratio
    if severity_medium_ratio is not None:
        over["severity_medium_ratio"] = severity_medium_ratio
    return {"metric": metric, "updated": over}


class DetectAnomalyRequest(BaseModel):
    """単一異常検知リクエスト"""

    metric: str
    value: float
    history: Optional[List[float]] = None


@router.post("/anomaly-detection/detect")
async def detect_anomaly(
    request: DetectAnomalyRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """単一値の異常検知（アンサンブル）"""
    config = _get_threshold_config(request.metric)
    result = ensemble_detect(
        request.value,
        request.metric,
        threshold_config=config,
        history=request.history,
    )
    return result


@router.get("/finops/cost-summary")
async def finops_cost_summary(
    period_days: int = 30,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """FinOps: クラウドコストサマリ・予測"""
    return get_cost_summary(period_days=period_days)


@router.get("/finops/cost-by-tag")
async def finops_cost_by_tag(
    tag_key: str = "project",
    period_days: int = 30,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """FinOps: タグ別コスト"""
    return {"items": get_cost_by_tag(tag_key, period_days)}


@router.post("/anomaly-detection/batch")
async def batch_anomaly_detection(
    request: BatchAnomalyRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """バッチ異常検知（医療・製造ドメイン）"""
    results = get_anomaly_list(request.domain, request.items)
    return {"items": results, "total": len(results)}
