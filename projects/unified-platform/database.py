"""Phase 1: Database - SQLAlchemy async + sync"""
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_config

cfg = get_config()
Base = declarative_base()

# Async (FastAPI)
_engine_kw = {"echo": cfg["debug"]}
if "sqlite" not in cfg["database_url"]:
    _engine_kw.update(pool_pre_ping=True, pool_size=5, max_overflow=10)
async_engine = create_async_engine(cfg["database_url"], **_engine_kw)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

# Sync (Alembic, migrations)
sync_engine = create_engine(cfg["database_url_sync"], echo=cfg["debug"])
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create tables if not exist"""
    import models  # noqa: F401 - register models
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_db_health():
    try:
        async with AsyncSessionLocal() as s:
            await s.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
