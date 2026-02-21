"""
キャッシュ戦略のテスト
"""
import time

import pytest

from core.cache import cache_strategy, cached, invalidate_cache


def test_cache_set_get():
    """キャッシュの設定と取得をテスト"""
    key = "test_key"
    value = {"test": "data"}

    cache_strategy.set(key, value, ttl=60)
    result = cache_strategy.get(key)

    assert result == value


def test_cache_expiration():
    """キャッシュの有効期限をテスト"""
    key = "expire_test"
    value = "test_value"

    cache_strategy.set(key, value, ttl=1)
    assert cache_strategy.get(key) == value

    time.sleep(2)
    assert cache_strategy.get(key) is None


def test_cache_delete():
    """キャッシュの削除をテスト"""
    key = "delete_test"
    value = "test_value"

    cache_strategy.set(key, value)
    assert cache_strategy.get(key) == value

    cache_strategy.delete(key)
    assert cache_strategy.get(key) is None


@cached(ttl=60, key_prefix="test_func")
def cached_function(x: int, y: int) -> int:
    """キャッシュされる関数"""
    return x + y


def test_cached_decorator():
    """キャッシュデコレータをテスト"""
    # 初回実行
    result1 = cached_function(1, 2)
    assert result1 == 3

    # 2回目はキャッシュから取得されるはず
    result2 = cached_function(1, 2)
    assert result2 == 3


def test_cache_stats():
    """キャッシュ統計をテスト"""
    stats = cache_strategy.get_stats()
    assert "enabled" in stats
    assert "total_keys" in stats
