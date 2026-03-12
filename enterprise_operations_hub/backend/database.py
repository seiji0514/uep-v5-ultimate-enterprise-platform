"""DB接続（SQLite/PostgreSQL）"""
import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# スキーマバージョン（変更時は既存DBを自動再作成）
SCHEMA_VERSION = 2

DATABASE_URL = os.environ.get(
    "EOH_DATABASE_URL",
    f"sqlite:///{Path(__file__).parent.parent / 'eoh.db'}",
)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_schema_version():
    """スキーマバージョン不一致時はDBを削除して再作成"""
    if "sqlite" not in DATABASE_URL:
        return
    db_path = Path(DATABASE_URL.replace("sqlite:///", ""))
    if not db_path.exists():
        return
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS schema_info (key TEXT PRIMARY KEY, value TEXT)"))
            r = conn.execute(text("SELECT value FROM schema_info WHERE key='version'")).fetchone()
            conn.commit()
            if r and int(r[0]) >= SCHEMA_VERSION:
                return
    except Exception:
        pass
    try:
        db_path.unlink(missing_ok=True)
    except OSError as e:
        import sys
        print(f"[EOH] スキーマ更新のため eoh.db の削除に失敗しました: {e}", file=sys.stderr)
        print("[EOH] バックエンドを停止し、enterprise_operations_hub/eoh.db を手動で削除してから再起動してください。", file=sys.stderr)


def set_schema_version():
    """スキーマバージョンを記録（create_all後に呼ぶ）"""
    if "sqlite" not in DATABASE_URL:
        return
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS schema_info (key TEXT PRIMARY KEY, value TEXT)"))
            conn.execute(text("INSERT OR REPLACE INTO schema_info (key, value) VALUES ('version', :v)"), {"v": str(SCHEMA_VERSION)})
            conn.commit()
    except Exception:
        pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
