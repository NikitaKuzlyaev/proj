import os
from typing import Any, AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = os.getenv("DATABASE_DEBUG_URL")
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


# sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), future=True)
# SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        yield session
