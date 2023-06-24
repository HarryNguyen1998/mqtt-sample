from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config

engine = create_async_engine(
    Config.DB_URL, connect_args={"connect_timeout": 10}
)

LocalSession = sessionmaker(bind=engine, class_=AsyncSession)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = LocalSession()
    try:
        yield session
    finally:
        await session.close()
