"""
SQLiteデータベース設定（Docker不要版）
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLiteを使用
DATABASE_URL = "sqlite:///./smart_city.db"

# データベースエンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite用
    echo=False  # SQLクエリをログ出力する場合はTrue
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


def init_db():
    """データベースの初期化"""
    Base.metadata.create_all(bind=engine)
    print("データベースを初期化しました: smart_city.db")

