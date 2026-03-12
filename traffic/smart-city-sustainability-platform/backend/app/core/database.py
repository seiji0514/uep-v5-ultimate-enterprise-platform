"""
データベース設定
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# データベースエンジンの作成
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデル
Base = declarative_base()


def get_db():
    """データベースセッションの取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

