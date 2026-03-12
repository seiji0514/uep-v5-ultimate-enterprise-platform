"""
Redis Streams クライアント
軽量イベントストリーム、Kafka 代替
補強スキル: Redis Streams、イベント駆動
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None


class RedisStreamsClient:
    """Redis Streams クライアント"""

    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 6379,
        db: int = 0,
    ):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", "6379"))
        self.db = db
        self._client: Optional[Any] = None

    def _get_client(self):
        if not REDIS_AVAILABLE:
            raise RuntimeError("Redis is not available. pip install redis")
        if self._client is None:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
            )
        return self._client

    def add(
        self,
        stream: str,
        data: Dict[str, Any],
        max_len: Optional[int] = 10000,
    ) -> str:
        """ストリームにメッセージを追加"""
        client = self._get_client()
        payload = {
            "data": json.dumps(data) if isinstance(data, dict) else str(data),
            "timestamp": datetime.utcnow().isoformat(),
        }
        kwargs = {"maxlen": max_len} if max_len else {}
        return client.xadd(stream, payload, **kwargs)

    def read(
        self,
        stream: str,
        last_id: str = "0",
        count: int = 10,
    ) -> List[Dict[str, Any]]:
        """ストリームからメッセージを読み取り"""
        client = self._get_client()
        result = client.xread({stream: last_id}, count=count, block=0)
        messages = []
        for sname, entries in result:
            for eid, fields in entries:
                messages.append({"id": eid, "data": fields})
        return messages

    def create_consumer_group(self, stream: str, group: str) -> bool:
        """コンシューマーグループを作成"""
        if not REDIS_AVAILABLE:
            return False
        try:
            client = self._get_client()
            client.xgroup_create(stream, group, "0", mkstream=True)
            return True
        except Exception:
            return False

    def close(self):
        """接続を閉じる"""
        if self._client:
            self._client.close()
            self._client = None
