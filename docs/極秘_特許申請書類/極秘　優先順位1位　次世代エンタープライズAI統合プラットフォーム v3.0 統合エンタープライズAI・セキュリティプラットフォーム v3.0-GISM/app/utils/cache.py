"""
キャッシュユーティリティ
- LRUキャッシュ
- TTL（Time To Live）キャッシュ
- メモリ効率的なキャッシュ管理
"""
import time
import hashlib
import json
from typing import Any, Optional, Callable, Dict
from functools import wraps
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class LRUCache:
    """LRU（Least Recently Used）キャッシュ"""
    
    def __init__(self, max_size: int = 100):
        """
        Args:
            max_size: 最大キャッシュサイズ
        """
        self.max_size = max_size
        self.cache = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """キャッシュから値を取得"""
        if key in self.cache:
            # アクセスしたアイテムを最後に移動（LRU）
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """キャッシュに値を設定"""
        if key in self.cache:
            # 既存のキーの場合は最後に移動
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.max_size:
            # キャッシュが満杯の場合は最初のアイテムを削除（LRU）
            self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def clear(self) -> None:
        """キャッシュをクリア"""
        self.cache.clear()
    
    def size(self) -> int:
        """キャッシュサイズを取得"""
        return len(self.cache)


class TTLCache:
    """TTL（Time To Live）キャッシュ"""
    
    def __init__(self, ttl_seconds: int = 3600, max_size: int = 100):
        """
        Args:
            ttl_seconds: TTL（秒）
            max_size: 最大キャッシュサイズ
        """
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key: str) -> Optional[Any]:
        """キャッシュから値を取得（TTLチェック付き）"""
        if key in self.cache:
            # TTLチェック
            if time.time() - self.timestamps[key] < self.ttl_seconds:
                return self.cache[key]
            else:
                # TTL切れの場合は削除
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """キャッシュに値を設定"""
        # キャッシュサイズチェック
        if len(self.cache) >= self.max_size and key not in self.cache:
            # 最も古いアイテムを削除
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self) -> None:
        """キャッシュをクリア"""
        self.cache.clear()
        self.timestamps.clear()
    
    def cleanup_expired(self) -> int:
        """期限切れアイテムをクリーンアップ"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.timestamps.items()
            if current_time - timestamp >= self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.timestamps[key]
        
        return len(expired_keys)


def cache_key(*args, **kwargs) -> str:
    """キャッシュキーを生成"""
    # 引数をシリアライズしてハッシュ化
    key_data = {
        "args": args,
        "kwargs": sorted(kwargs.items())
    }
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(max_size: int = 100, ttl_seconds: Optional[int] = None):
    """
    関数結果をキャッシュするデコレータ
    
    Args:
        max_size: 最大キャッシュサイズ（LRUキャッシュの場合）
        ttl_seconds: TTL（秒、Noneの場合はLRUキャッシュを使用）
    """
    cache = TTLCache(ttl_seconds=ttl_seconds or 3600, max_size=max_size) if ttl_seconds else LRUCache(max_size=max_size)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_key(*args, **kwargs)
            result = cache.get(key)
            
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result
            
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        wrapper.cache = cache  # キャッシュオブジェクトにアクセス可能にする
        return wrapper
    
    return decorator


class CacheManager:
    """キャッシュマネージャー（複数のキャッシュを管理）"""
    
    def __init__(self):
        self.caches = {}
    
    def get_cache(self, name: str, cache_type: str = "lru", **kwargs) -> Any:
        """
        キャッシュを取得または作成
        
        Args:
            name: キャッシュ名
            cache_type: キャッシュタイプ（"lru" or "ttl"）
            **kwargs: キャッシュの初期化パラメータ
        """
        if name not in self.caches:
            if cache_type == "ttl":
                self.caches[name] = TTLCache(**kwargs)
            else:
                self.caches[name] = LRUCache(**kwargs)
        
        return self.caches[name]
    
    def clear_all(self) -> None:
        """全キャッシュをクリア"""
        for cache in self.caches.values():
            cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """全キャッシュの統計情報を取得"""
        stats = {}
        for name, cache in self.caches.items():
            if isinstance(cache, LRUCache):
                stats[name] = {
                    "type": "LRU",
                    "size": cache.size(),
                    "max_size": cache.max_size
                }
            elif isinstance(cache, TTLCache):
                stats[name] = {
                    "type": "TTL",
                    "size": len(cache.cache),
                    "max_size": cache.max_size,
                    "ttl_seconds": cache.ttl_seconds
                }
        return stats


# グローバルキャッシュマネージャー
cache_manager = CacheManager()

