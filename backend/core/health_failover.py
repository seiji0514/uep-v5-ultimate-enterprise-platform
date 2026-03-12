"""
稼働率向上モジュール
冗長化、フェイルオーバー、監視の強化
"""
import asyncio
import time
from typing import Any, Callable, Dict, List, Optional

# ヘルスチェック設定
HEALTH_CHECK_TIMEOUT = 5.0
HEALTH_CHECK_RETRIES = 3
FAILOVER_RETRY_DELAY = 1.0


async def health_check_with_retry(
    check_fn: Callable,
    retries: int = HEALTH_CHECK_RETRIES,
    timeout: float = HEALTH_CHECK_TIMEOUT,
) -> Dict[str, Any]:
    """
    リトライ付きヘルスチェック

    Args:
        check_fn: 非同期ヘルスチェック関数（引数なし、Dict を返す）
        retries: リトライ回数
        timeout: タイムアウト秒

    Returns:
        ヘルスチェック結果
    """
    last_error = None
    for attempt in range(retries):
        try:
            result = await asyncio.wait_for(check_fn(), timeout=timeout)
            return {
                "status": "healthy",
                "attempt": attempt + 1,
                "result": result,
            }
        except asyncio.TimeoutError as e:
            last_error = e
            if attempt < retries - 1:
                await asyncio.sleep(FAILOVER_RETRY_DELAY)
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                await asyncio.sleep(FAILOVER_RETRY_DELAY)

    return {
        "status": "unhealthy",
        "attempts": retries,
        "error": str(last_error) if last_error else "Unknown",
    }


async def failover_execute(
    primary_fn: Callable,
    fallback_fn: Optional[Callable] = None,
    fallback_value: Any = None,
) -> Any:
    """
    フェイルオーバー実行: プライマリ失敗時にフォールバックを実行

    Args:
        primary_fn: 非同期プライマリ処理
        fallback_fn: フォールバック処理（None の場合は fallback_value を返す）
        fallback_value: フォールバック関数が None の場合の戻り値

    Returns:
        プライマリまたはフォールバックの結果
    """
    try:
        return await primary_fn()
    except Exception:
        if fallback_fn:
            try:
                return await fallback_fn()
            except Exception:
                return fallback_value
    return fallback_value


class ServiceHealthRegistry:
    """サービスヘルスレジストリ（監視強化）"""

    def __init__(self):
        self._services: Dict[str, Dict[str, Any]] = {}
        self._last_checks: Dict[str, float] = {}

    def register(self, name: str, check_url: str, priority: int = 0):
        """サービスを登録"""
        self._services[name] = {
            "check_url": check_url,
            "priority": priority,
            "status": "unknown",
            "last_check": None,
        }

    def update_status(self, name: str, status: str, latency_ms: Optional[float] = None):
        """ステータスを更新"""
        if name in self._services:
            self._services[name]["status"] = status
            self._services[name]["last_check"] = time.time()
            if latency_ms is not None:
                self._services[name]["latency_ms"] = latency_ms

    def get_healthy_services(self) -> List[str]:
        """健全なサービスのリストを取得"""
        return [
            name
            for name, data in self._services.items()
            if data.get("status") == "healthy"
        ]

    def get_all_status(self) -> Dict[str, Any]:
        """全サービスのステータスを取得"""
        return dict(self._services)


# グローバルレジストリ
service_health_registry = ServiceHealthRegistry()
