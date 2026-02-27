from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from project.core.config import settings


class Base(DeclarativeBase, AsyncAttrs):
    pass


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
