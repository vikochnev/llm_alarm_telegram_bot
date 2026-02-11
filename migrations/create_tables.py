import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.infrastructure.database.core import engine, Base
from app.infrastructure.database.models import User, Alarm  # НЕ УДАЛЯТЬ ЭТИ ИМПОРТЫ!

from config.config import load_config
from logging import getLogger

config = load_config()
logger = getLogger(__name__)


async def create_db():
    logger.debug('Creating engine for initialing a database...')
    db_create_engine = create_async_engine(
        config.orm.base_url.replace("/alarms_bot_db", "/postgres"),
        isolation_level="AUTOCOMMIT",
    )
    logger.debug('Engine created...')
    async with db_create_engine.begin() as conn:
        logger.debug('Trying to create database...')
        try:
            await conn.execute(text("CREATE DATABASE alarms_bot_db"))
        except Exception as e:
            if "already exists" not in str(e):
                logger.exception(e)
    await db_create_engine.dispose()
    logger.debug('Engine successfully disposed...')


async def init_models():
    logger.debug('Creating tables...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    logger.info('Creating a db and tables...')
    asyncio.run(create_db())
    asyncio.run(init_models())
