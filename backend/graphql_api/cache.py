"""
GraphQL キャッシュ戦略
補強スキル: GraphQL キャッシュ
"""
import os
from typing import Any, Optional

# インメモリキャッシュ（本番では Redis 等を推奨）
_cache: dict = {}
_cache_ttl: dict = {}
_DEFAULT_TTL = int(os.getenv("GRAPHQL_CACHE_TTL_SEC", "60"))


def get_cached(key: str) -> Optional[Any]:
    """キャッシュから取得"""
    import time

    if key not in _cache:
        return None
    ttl = _cache_ttl.get(key, 0)
    if ttl and time.time() > ttl:
        del _cache[key]
        del _cache_ttl[key]
        return None
    return _cache[key]


def set_cached(key: str, value: Any, ttl_sec: int = _DEFAULT_TTL) -> None:
    """キャッシュに保存"""
    import time

    _cache[key] = value
    _cache_ttl[key] = time.time() + ttl_sec if ttl_sec > 0 else 0


def invalidate_cached(prefix: Optional[str] = None) -> int:
    """キャッシュ無効化（prefix 指定時は前方一致）"""
    global _cache, _cache_ttl
    if prefix is None:
        count = len(_cache)
        _cache.clear()
        _cache_ttl.clear()
        return count
    keys = [k for k in _cache if k.startswith(prefix)]
    for k in keys:
        del _cache[k]
        del _cache_ttl[k]
    return len(keys)
