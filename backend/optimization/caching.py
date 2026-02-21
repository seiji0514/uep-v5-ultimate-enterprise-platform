"""
キャッシュ管理モジュール
"""
import hashlib
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class CacheManager:
    """キャッシュ管理クラス"""

    def __init__(self):
        """キャッシュマネージャーを初期化"""
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = 300  # デフォルトTTL（秒）

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """キャッシュキーを生成"""
        key_data = {"prefix": prefix, "args": args, "kwargs": kwargs}
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """キャッシュから取得"""
        cached_item = self._cache.get(key)
        if not cached_item:
            return None

        # TTLチェック
        if datetime.utcnow() > cached_item["expires_at"]:
            del self._cache[key]
            return None

        return cached_item["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """キャッシュに設定"""
        ttl = ttl or self._default_ttl
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)

        self._cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": datetime.utcnow(),
        }

    def delete(self, key: str) -> bool:
        """キャッシュを削除"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self, prefix: Optional[str] = None):
        """キャッシュをクリア"""
        if prefix:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(prefix)]
            for key in keys_to_delete:
                del self._cache[key]
        else:
            self._cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """キャッシュ統計を取得"""
        total_items = len(self._cache)
        expired_items = sum(
            1 for item in self._cache.values() if datetime.utcnow() > item["expires_at"]
        )

        return {
            "total_items": total_items,
            "active_items": total_items - expired_items,
            "expired_items": expired_items,
            "cache_size_mb": 0,  # 簡易実装
        }


# グローバルインスタンス
cache_manager = CacheManager()
