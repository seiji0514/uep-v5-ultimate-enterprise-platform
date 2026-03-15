"""
APIレート制限モジュール
slowapiを使用した高度なレート制限
"""
import logging
from typing import Callable

from fastapi import Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from core.config import settings

logger = logging.getLogger(__name__)


def get_limiter_key(request: Request) -> str:
    """レート制限のキーを取得"""
    # 認証済みユーザーの場合はユーザーIDを使用
    if hasattr(request.state, "user") and request.state.user:
        return request.state.user.get("username", get_remote_address(request))
    return get_remote_address(request)


def _get_storage_uri() -> str:
    """Redis接続可能ならRedis、不可ならメモリを使用"""
    if not settings.RATE_LIMIT_ENABLED:
        return "memory://"
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL)
        try:
            r.ping()
            return settings.REDIS_URL
        finally:
            r.close()
    except Exception as e:
        logger.warning("Redis接続不可のためメモリストレージを使用します: %s", e)
        return "memory://"


# Limiterインスタンスの作成（Redis未起動時はメモリにフォールバック）
limiter = Limiter(
    key_func=get_limiter_key,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
    storage_uri=_get_storage_uri(),
    headers_enabled=True,
)


def rate_limit(calls: int = 60, period: int = 60):
    """
    レート制限デコレータ

    Usage:
        @app.get("/api/v1/endpoint")
        @rate_limit(calls=10, period=60)  # 60秒間に10回
        async def endpoint():
            return {"message": "OK"}
    """

    def decorator(func: Callable):
        return limiter.limit(f"{calls}/{period}seconds")(func)

    return decorator
