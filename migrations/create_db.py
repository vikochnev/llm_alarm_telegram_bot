import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

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


if __name__ == '__main__':
    asyncio.run(create_db())
