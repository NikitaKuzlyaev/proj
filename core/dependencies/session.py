from typing import AsyncGenerator

from core.database.connection import get_session


async def get_async_session() -> AsyncGenerator:
    async for session in get_session():
        yield session
