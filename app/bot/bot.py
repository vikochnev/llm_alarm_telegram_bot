import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import Config
from app.bot.scheduler.scheduler import scheduler
from app.bot.handlers.menu_commands import menu_commands_router
from app.bot.handlers.others import others_router


logger = logging.getLogger(__name__)


async def main(config: Config) -> None:
    logger.info("Starting bot...")

    # Initialising bot and dispatcher
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

    scheduler.start()
    logger.debug('Scheduler started...')

    # Запускаем поллинг
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)