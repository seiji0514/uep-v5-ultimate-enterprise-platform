"""Phase 2: Redis - Cache, Session"""
from typing import Optional, Any
import json
import redis.asyncio as redis
from config import get_config

_cached_client: Optional[redis.Redis] = None


async def get_redis() -> Optional[redis.Redis]:
    global _cached_client
    if _cached_client is None:
        try:
            _cached_client = redis.from_url(
                get_config()["redis_url"],
                encoding="utf-8",
                decode_responses=True,
            )
        except Exception:
            return None
    return _cached_client


async def cache_get(key: str) -> Optional[Any]:
    r = await get_redis()
    if not r:
        return None
    try:
        val = await r.get(key)
        if val:
            return json.loads(val)
    except Exception:
        pass
    return None


async def cache_set(key: str, value: Any, ttl_sec: int = 300) -> bool:
    r = await get_redis()
    if not r:
        return False
    try:
        await r.setex(key, ttl_sec, json.dumps(value, default=str))
        return True
    except Exception:
        return False


async def login_attempt_incr(key: str, ttl_sec: int = 900) -> int:
    """ログイン試行回数をインクリメント。戻り値は現在の試行回数"""
    r = await get_redis()
    if not r:
        return 0
    try:
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, ttl_sec)
        result = await pipe.execute()
        return int(result[0]) if result else 0
    except Exception:
        return 0


async def login_attempt_reset(key: str) -> None:
    r = await get_redis()
    if r:
        try:
            await r.delete(key)
        except Exception:
            pass


async def is_login_locked(key: str) -> bool:
    r = await get_redis()
    if not r:
        return False
    try:
        val = await r.get(key)
        return val is not None and int(val or 0) >= get_config().get("login_max_attempts", 5)
    except Exception:
        return False


async def notification_mark_read(user_id: str, notif_id: int) -> None:
    """通知を既読にする"""
    r = await get_redis()
    if r:
        try:
            key = f"notif_read:{user_id}"
            await r.sadd(key, str(notif_id))
            await r.expire(key, 86400 * 30)  # 30日
        except Exception:
            pass


async def notification_read_ids(user_id: str) -> set:
    """既読通知ID一覧"""
    r = await get_redis()
    if not r:
        return set()
    try:
        members = await r.smembers(f"notif_read:{user_id}")
        return {int(x) for x in members if x.isdigit()}
    except Exception:
        return set()
