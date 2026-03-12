"""
AI利用ログ記録
推論・学習の全ログを記録・監査可能
"""
import uuid
from collections import deque
from datetime import datetime
from typing import Any, Dict, List
import threading

# スレッドセーフなログストア（メモリ、最大1000件）
_log_store: deque = deque(maxlen=1000)
_lock = threading.Lock()


def log_ai_usage(
    operation: str,
    model: str,
    user_id: str,
    input_summary: str = "",
    output_summary: str = "",
    risk_level: str = "low",
    metadata: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    AI利用をログに記録

    Args:
        operation: 操作種別（generate, rag, reasoning, routing 等）
        model: モデル名
        user_id: ユーザーID
        input_summary: 入力の要約（先頭100文字等）
        output_summary: 出力の要約
        risk_level: リスクレベル（low, medium, high）
        metadata: 追加メタデータ

    Returns:
        記録されたログエントリ
    """
    entry = {
        "id": f"log_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "operation": operation,
        "model": model,
        "user_id": user_id,
        "input_summary": input_summary[:200] if input_summary else "",
        "output_summary": output_summary[:200] if output_summary else "",
        "risk_level": risk_level,
        "metadata": metadata or {},
    }
    with _lock:
        _log_store.append(entry)
    return entry


def get_ai_usage_logs(limit: int = 100, user_id: str | None = None) -> List[Dict[str, Any]]:
    """ログを取得（監査用）"""
    with _lock:
        logs = list(_log_store)
    if user_id:
        logs = [l for l in logs if l.get("user_id") == user_id]
    return list(reversed(logs[-limit:]))


def assess_risk(input_text: str, operation: str) -> str:
    """
    簡易リスク評価（EU AI Act リスクレベル風）

    Returns:
        low, medium, high
    """
    high_risk_keywords = ["医療", "法律", "金融", "採用", "信用", "medical", "legal", "finance"]
    medium_risk_keywords = ["個人", "評価", "判断", "personal", "evaluation"]

    lower = input_text.lower()
    for kw in high_risk_keywords:
        if kw in input_text or kw in lower:
            return "high"
    for kw in medium_risk_keywords:
        if kw in input_text or kw in lower:
            return "medium"
    return "low"
