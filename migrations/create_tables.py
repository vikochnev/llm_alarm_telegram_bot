import asyncio

from app.infrastructure.database.core import engine, Base
from app.infrastructure.database.models import User, Alarm  # DO NOT DELETE THIS IMPORTS!!!!

from config.config import load_config
from logging import getLogger

config = load_config()
logger = getLogger(__name__)


async def init_models():
    logger.debug('Creating tables...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(init_models())
