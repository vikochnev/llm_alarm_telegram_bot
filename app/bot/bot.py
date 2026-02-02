import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import Config
from app.bot.services.alarm_checker import alarm_checker
from app.bot.handlers.menu_commands import menu_commands_router
from app.bot.handlers.others import others_router

logger = logging.getLogger(__name__)


async def main(config: Config) -> None:
    logger.info("Starting bot...")

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Получаем роутеры в нужном порядке
    logger.info("Including Routers...")
    dp.include_routers(
        menu_commands_router,
        others_router,
    )

    asyncio.create_task(alarm_checker(bot))

    # Запускаем поллинг
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)

    # Запускаем проверку алармов



