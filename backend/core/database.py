"""
データベース接続管理モジュール
SQLAlchemy + SQLite/PostgreSQL統合
"""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool, StaticPool


# core.config を遅延インポート（循環参照回避）
def _get_database_url() -> str:
    from core.config import settings

    return settings.DATABASE_URL


DATABASE_URL = _get_database_url()

# SQLiteの場合は接続プール設定を簡素化
_engine_kwargs = dict(pool_pre_ping=True, echo=False, future=True)
if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
    _engine_kwargs["poolclass"] = StaticPool
else:
    _engine_kwargs["poolclass"] = QueuePool
    _engine_kwargs["pool_size"] = 20
    _engine_kwargs["max_overflow"] = 40
    _engine_kwargs["pool_recycle"] = 3600

engine = create_engine(DATABASE_URL, **_engine_kwargs)

# セッションファクトリ
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

# ベースクラス
Base = declarative_base()

# メタデータ
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    データベースセッションを取得

    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    コンテキストマネージャーとしてデータベースセッションを取得

    Usage:
        with get_db_context() as db:
            item = Item(name="test")
            db.add(item)
            db.commit()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """データベーステーブルを作成"""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """データベーステーブルを削除（開発用）"""
    Base.metadata.drop_all(bind=engine)
