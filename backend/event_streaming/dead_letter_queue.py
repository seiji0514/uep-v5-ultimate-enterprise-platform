"""
デッドレターキュー (DLQ)
処理失敗メッセージの格納・再処理
補強スキル: イベント駆動、デッドレターキュー
"""
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# インメモリ DLQ（本番では Kafka DLQ トピックや Redis 等を推奨）
_dlq_store: List[Dict[str, Any]] = []
_DLQ_MAX_SIZE = int(os.getenv("DLQ_MAX_SIZE", "10000"))


def push_to_dlq(
    topic: str,
    event: Dict[str, Any],
    error: str,
    partition: Optional[int] = None,
    offset: Optional[int] = None,
) -> str:
    """
    失敗メッセージを DLQ に格納

    Args:
        topic: 元トピック
        event: イベントペイロード
        error: エラー内容
        partition: パーティション（任意）
        offset: オフセット（任意）

    Returns:
        DLQ エントリ ID
    """
    import uuid

    entry_id = str(uuid.uuid4())
    entry = {
        "id": entry_id,
        "topic": topic,
        "event": event,
        "error": error,
        "partition": partition,
        "offset": offset,
        "created_at": datetime.utcnow().isoformat(),
        "retry_count": 0,
    }
    global _dlq_store
    _dlq_store.append(entry)
    if len(_dlq_store) > _DLQ_MAX_SIZE:
        _dlq_store = _dlq_store[-_DLQ_MAX_SIZE:]
    logger.warning(f"DLQ pushed: {entry_id} topic={topic} error={error}")
    return entry_id


def list_dlq(limit: int = 100) -> List[Dict[str, Any]]:
    """DLQ 一覧を取得"""
    return list(reversed(_dlq_store[-limit:]))


def get_dlq_entry(entry_id: str) -> Optional[Dict[str, Any]]:
    """DLQ エントリを取得"""
    for e in _dlq_store:
        if e["id"] == entry_id:
            return e
    return None


def remove_from_dlq(entry_id: str) -> bool:
    """DLQ から削除（再処理成功時等）"""
    global _dlq_store
    for i, e in enumerate(_dlq_store):
        if e["id"] == entry_id:
            _dlq_store.pop(i)
            return True
    return False


def dlq_stats() -> Dict[str, Any]:
    """DLQ 統計"""
    return {
        "count": len(_dlq_store),
        "max_size": _DLQ_MAX_SIZE,
    }
