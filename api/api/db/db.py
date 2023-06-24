from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(Config.DB_URL, connect_args={"connect_timeout": 10})

LocalSession = sessionmaker(bind=engine, class_=AsyncSession)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a DB session that will close automatically when it's out of scope."""
    session = LocalSession()
    try:
        yield session
    finally:
        await session.close()
