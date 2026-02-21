"""
高度なキャッシング戦略モジュール
Redisベースのマルチレベルキャッシング
"""
from typing import Optional, Any, Callable, Dict
from functools import wraps
import json
import hashlib
import pickle
from datetime import datetime, timedelta
import redis
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class CacheStrategy:
    """キャッシュ戦略クラス"""

    def __init__(self):
        """キャッシュ戦略を初期化"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                password=settings.REDIS_PASSWORD,
                decode_responses=False,  # バイナリデータを扱うため
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # 接続テスト
            self.redis_client.ping()
            self.enabled = True
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Using in-memory cache.")
            self.redis_client = None
            self.enabled = False
            self._memory_cache: Dict[str, Any] = {}

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """キャッシュキーを生成"""
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return f"{prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"

    def get(self, key: str) -> Optional[Any]:
        """キャッシュから取得"""
        if not self.enabled:
            return self._memory_cache.get(key)

        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return pickle.loads(cached_data)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[list] = None
    ):
        """キャッシュに設定"""
        try:
            serialized_value = pickle.dumps(value)

            if self.enabled:
                if ttl:
                    self.redis_client.setex(key, ttl, serialized_value)
                else:
                    self.redis_client.set(key, serialized_value)

                # タグ管理（タグでグループ化されたキーを管理）
                if tags:
                    for tag in tags:
                        tag_key = f"tag:{tag}"
                        self.redis_client.sadd(tag_key, key)
                        if ttl:
                            self.redis_client.expire(tag_key, ttl)
            else:
                self._memory_cache[key] = value
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def delete(self, key: str) -> bool:
        """キャッシュを削除"""
        try:
            if self.enabled:
                return bool(self.redis_client.delete(key))
            else:
                return self._memory_cache.pop(key, None) is not None
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def delete_by_tag(self, tag: str) -> int:
        """タグでグループ化されたキャッシュを削除"""
        if not self.enabled:
            return 0

        try:
            tag_key = f"tag:{tag}"
            keys = self.redis_client.smembers(tag_key)
            if keys:
                deleted = self.redis_client.delete(*keys)
                self.redis_client.delete(tag_key)
                return deleted
        except Exception as e:
            logger.error(f"Cache delete by tag error: {e}")
        return 0

    def clear(self, pattern: Optional[str] = None):
        """キャッシュをクリア"""
        try:
            if self.enabled:
                if pattern:
                    keys = self.redis_client.keys(pattern)
                    if keys:
                        self.redis_client.delete(*keys)
                else:
                    self.redis_client.flushdb()
            else:
                if pattern:
                    self._memory_cache = {
                        k: v for k, v in self._memory_cache.items()
                        if pattern in k
                    }
                else:
                    self._memory_cache.clear()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """キャッシュ統計を取得"""
        try:
            if self.enabled:
                info = self.redis_client.info("stats")
                return {
                    "enabled": True,
                    "total_keys": self.redis_client.dbsize(),
                    "hits": info.get("keyspace_hits", 0),
                    "misses": info.get("keyspace_misses", 0),
                    "hit_rate": (
                        info.get("keyspace_hits", 0) /
                        (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1))
                    ) * 100
                }
            else:
                return {
                    "enabled": False,
                    "total_keys": len(self._memory_cache),
                    "hits": 0,
                    "misses": 0,
                    "hit_rate": 0
                }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"enabled": False, "error": str(e)}


# グローバルインスタンス
cache_strategy = CacheStrategy()


def cached(
    ttl: int = 300,
    key_prefix: str = "cache",
    tags: Optional[list] = None
):
    """
    関数結果をキャッシュするデコレータ

    Usage:
        @cached(ttl=600, tags=["users"])
        def get_user(user_id: int):
            return db.query(User).filter(User.id == user_id).first()
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = cache_strategy._generate_key(key_prefix, *args, **kwargs)

            # キャッシュから取得を試みる
            cached_value = cache_strategy.get(cache_key)
            if cached_value is not None:
                return cached_value

            # キャッシュにない場合は関数を実行
            result = await func(*args, **kwargs)

            # 結果をキャッシュ
            cache_strategy.set(cache_key, result, ttl=ttl, tags=tags)

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = cache_strategy._generate_key(key_prefix, *args, **kwargs)

            # キャッシュから取得を試みる
            cached_value = cache_strategy.get(cache_key)
            if cached_value is not None:
                return cached_value

            # キャッシュにない場合は関数を実行
            result = func(*args, **kwargs)

            # 結果をキャッシュ
            cache_strategy.set(cache_key, result, ttl=ttl, tags=tags)

            return result

        # 非同期関数かどうかでラッパーを選択
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def invalidate_cache(pattern: Optional[str] = None, tag: Optional[str] = None):
    """キャッシュを無効化"""
    if tag:
        cache_strategy.delete_by_tag(tag)
    elif pattern:
        cache_strategy.clear(pattern)
    else:
        cache_strategy.clear()
