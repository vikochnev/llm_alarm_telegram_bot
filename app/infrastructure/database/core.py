from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config.config import load_config

config = load_config()

DATABASE_URL = config.orm.base_url

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session_maker() as session:
        yield session
