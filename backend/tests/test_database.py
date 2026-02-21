"""
データベース接続のテスト
"""
import pytest
from sqlalchemy.orm import Session

from core.database import SessionLocal, get_db, init_db


def test_database_connection():
    """データベース接続をテスト"""
    db = SessionLocal()
    try:
        # 接続テスト
        result = db.execute("SELECT 1")
        assert result.scalar() == 1
    finally:
        db.close()


def test_get_db():
    """get_db関数をテスト"""
    db_gen = get_db()
    db = next(db_gen)

    assert db is not None
    assert isinstance(db, Session)

    # クリーンアップ
    try:
        next(db_gen)
    except StopIteration:
        pass
