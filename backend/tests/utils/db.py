# tests/utils/db.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from libs.common.base import Base

# ------------------------------------------
# CREATE ASYNC TEST DATABASE (SQLite Memory)
# ------------------------------------------
# For PostgreSQL during CI/CD, use:
# postgresql+asyncpg://test:test@localhost:5432/test_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

AsyncTestingSessionLocal = sessionmaker(
    engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_test_db():
    """
    Create all tables in the in-memory DB.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_test_db():
    """
    Drop tables after tests.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    """
    Replacement for get_db() inside FastAPI services.
    """
    async with AsyncTestingSessionLocal() as session:
        yield session
