"""
異常検知サービス
閾値調整、特徴量追加、モデルアンサンブル
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class ThresholdConfig:
    """閾値設定（ドメイン別に調整可能）"""

    metric: str
    upper: float
    lower: float
    severity_high_ratio: float = 1.5  # 閾値の何倍で「高」とするか
    severity_medium_ratio: float = 1.2


# デフォルト閾値（医療・製造で共通利用可能）
DEFAULT_THRESHOLDS: Dict[str, ThresholdConfig] = {
    "heart_rate": ThresholdConfig("心拍数", 100, 50, 1.5, 1.2),
    "blood_glucose": ThresholdConfig("血糖値", 200, 0, 1.4, 1.2),
    "temperature": ThresholdConfig("体温", 38.0, 35.0, 1.05, 1.02),
    "temperature_equipment": ThresholdConfig("設備温度", 85.0, 0, 1.2, 1.1),
    "vibration": ThresholdConfig("振動", 0.15, 0, 2.0, 1.5),
    "pressure": ThresholdConfig("圧力", 6.0, 0, 1.5, 1.2),
}


def _threshold_detector(value: float, config: ThresholdConfig) -> Dict[str, Any]:
    """閾値ベースの異常検知"""
    if value > config.upper or value < config.lower:
        ratio = (
            value / config.upper
            if value > config.upper
            else config.lower / max(value, 0.001)
        )
        if ratio >= config.severity_high_ratio:
            severity = "高"
        elif ratio >= config.severity_medium_ratio:
            severity = "中"
        else:
            severity = "低"
        return {
            "is_anomaly": True,
            "severity": severity,
            "threshold": config.upper if value > config.upper else config.lower,
            "method": "threshold",
        }
    return {"is_anomaly": False, "method": "threshold"}


def _zscore_detector(
    value: float, mean: float, std: float, z_threshold: float = 3.0
) -> Dict[str, Any]:
    """Z-scoreベースの異常検知（特徴量: 統計的逸脱）"""
    if std <= 0:
        return {"is_anomaly": False, "method": "zscore"}
    z = abs(value - mean) / std
    if z >= z_threshold:
        severity = "高" if z >= z_threshold * 1.5 else "中"
        return {
            "is_anomaly": True,
            "severity": severity,
            "z_score": round(z, 2),
            "method": "zscore",
        }
    return {"is_anomaly": False, "method": "zscore"}


def _rolling_detector(
    value: float, history: List[float], window: int = 10, deviation: float = 2.0
) -> Dict[str, Any]:
    """ローリング統計ベースの異常検知（特徴量: 時系列変化）"""
    if len(history) < window:
        return {"is_anomaly": False, "method": "rolling"}
    recent = history[-window:]
    mean = sum(recent) / len(recent)
    variance = sum((x - mean) ** 2 for x in recent) / len(recent)
    std = variance**0.5 if variance > 0 else 0
    return _zscore_detector(value, mean, std, z_threshold=deviation)


def ensemble_detect(
    value: float,
    metric_type: str,
    threshold_config: Optional[ThresholdConfig] = None,
    history: Optional[List[float]] = None,
    zscore_params: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    モデルアンサンブルによる異常検知

    Args:
        value: 測定値
        metric_type: メトリック種別（heart_rate, blood_glucose, vibration 等）
        threshold_config: 閾値設定（None でデフォルト使用）
        history: 時系列履歴（ローリング検知用）
        zscore_params: 平均・標準偏差（Z-score検知用）

    Returns:
        検知結果（アンサンブル投票）
    """
    config = threshold_config or DEFAULT_THRESHOLDS.get(
        metric_type, ThresholdConfig(metric_type, float("inf"), float("-inf"))
    )

    results: List[Dict[str, Any]] = []

    # 1. 閾値検知
    r1 = _threshold_detector(value, config)
    results.append(r1)

    # 2. Z-score検知（パラメータがある場合）
    if zscore_params:
        r2 = _zscore_detector(
            value,
            zscore_params.get("mean", value),
            zscore_params.get("std", 1.0),
            zscore_params.get("threshold", 3.0),
        )
        results.append(r2)

    # 3. ローリング検知（履歴がある場合）
    if history:
        r3 = _rolling_detector(value, history)
        results.append(r3)

    # アンサンブル投票: 多数決
    anomalies = [r for r in results if r.get("is_anomaly")]
    is_anomaly = len(anomalies) >= max(1, len(results) // 2)
    severity = "高"
    if anomalies:
        sevs = [a.get("severity", "中") for a in anomalies]
        if "高" in sevs:
            severity = "高"
        elif "中" in sevs:
            severity = "中"
        else:
            severity = "低"

    return {
        "is_anomaly": is_anomaly,
        "severity": severity if is_anomaly else None,
        "value": value,
        "metric": config.metric,
        "ensemble_votes": len(anomalies),
        "ensemble_total": len(results),
        "detectors": [r.get("method") for r in results],
        "detected_at": datetime.now(timezone.utc).isoformat(),
    }


def get_anomaly_list(
    domain: str,
    items: List[Dict[str, Any]],
    thresholds: Optional[Dict[str, ThresholdConfig]] = None,
) -> List[Dict[str, Any]]:
    """
    既存データに対して異常検知を実行し、異常一覧を返す

    Args:
        domain: ドメイン（medical, manufacturing）
        items: センサーデータ等のリスト
        thresholds: カスタム閾値

    Returns:
        異常検知結果のリスト
    """
    if domain == "medical":
        default_items = [
            {
                "id": "ma-001",
                "metric": "heart_rate",
                "value": 125,
                "patient_id": "P001",
            },
            {
                "id": "ma-002",
                "metric": "blood_glucose",
                "value": 280,
                "patient_id": "P002",
            },
        ]
    else:
        default_items = [
            {
                "id": "ano-001",
                "metric": "vibration",
                "value": 0.25,
                "equipment": "CNC旋盤A",
            },
            {
                "id": "ano-002",
                "metric": "temperature_equipment",
                "value": 95.0,
                "equipment": "溶接ロボットB",
            },
        ]

    data = items if items else default_items
    configs = thresholds or DEFAULT_THRESHOLDS
    results = []

    for item in data:
        metric = item.get("metric", "unknown")
        value = item.get("value", 0)
        config = (
            configs.get(metric)
            if isinstance(configs.get(metric), ThresholdConfig)
            else None
        )
        if not config:
            config = DEFAULT_THRESHOLDS.get(metric, ThresholdConfig(metric, 999, -999))

        det = ensemble_detect(value, metric, threshold_config=config)
        if det["is_anomaly"]:
            results.append(
                {
                    **item,
                    "type": f"{config.metric}異常",
                    "severity": det["severity"],
                    "detected_at": det["detected_at"],
                    "ensemble_votes": det.get("ensemble_votes", 1),
                }
            )

    return results
