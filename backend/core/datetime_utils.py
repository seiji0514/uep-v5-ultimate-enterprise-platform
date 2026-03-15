"""
datetime ユーティリティ
Python 3.12+ の datetime.utcnow() DeprecationWarning 対応
"""
from datetime import datetime, timezone


def utc_now() -> datetime:
    """現在の UTC 時刻を返す。datetime.utcnow() の代替。"""
    return datetime.now(timezone.utc)
