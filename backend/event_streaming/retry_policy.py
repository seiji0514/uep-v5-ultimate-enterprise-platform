"""
リトライポリシー
イベント処理失敗時の指数バックオフ等
補強スキル: イベント駆動、リトライポリシー
"""
import math
import random
import time
from dataclasses import dataclass
from typing import Callable, Optional, TypeVar

T = TypeVar("T")


@dataclass
class RetryPolicy:
    """リトライポリシー設定"""

    max_retries: int = 3
    initial_delay_sec: float = 1.0
    max_delay_sec: float = 60.0
    backoff_multiplier: float = 2.0
    jitter: bool = True

    def get_delay(self, attempt: int) -> float:
        """attempt 回目のリトライまでの待機時間（秒）"""
        delay = min(
            self.initial_delay_sec * (self.backoff_multiplier ** attempt),
            self.max_delay_sec,
        )
        if self.jitter:
            delay *= 0.5 + 0.5 * random.random()
        return delay


def retry_with_policy(
    fn: Callable[[], T],
    policy: Optional[RetryPolicy] = None,
    on_retry: Optional[Callable[[Exception, int], None]] = None,
) -> T:
    """
    リトライポリシー付きで関数を実行

    Args:
        fn: 実行する関数（引数なし）
        policy: リトライポリシー（None の場合はデフォルト）
        on_retry: リトライ時のコールバック (exception, attempt)

    Returns:
        関数の戻り値

    Raises:
        最後の試行で発生した例外
    """
    p = policy or RetryPolicy()
    last_exc = None
    for attempt in range(p.max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt >= p.max_retries:
                raise
            delay = p.get_delay(attempt)
            if on_retry:
                on_retry(e, attempt)
            time.sleep(delay)
    raise last_exc


async def retry_async(
    fn: Callable,
    policy: Optional[RetryPolicy] = None,
    on_retry: Optional[Callable[[Exception, int], None]] = None,
):
    """非同期版リトライ"""
    import asyncio
    p = policy or RetryPolicy()
    last_exc = None
    for attempt in range(p.max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(fn):
                return await fn()
            return fn()
        except Exception as e:
            last_exc = e
            if attempt >= p.max_retries:
                raise
            delay = p.get_delay(attempt)
            if on_retry:
                on_retry(e, attempt)
            await asyncio.sleep(delay)
    raise last_exc
