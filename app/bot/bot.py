import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.scheduler.scheduler import scheduler
from app.bot.services.database_parsers import delete_due_alarms, hard_delete_soft_deleted_alarms
from app.bot.scheduler.scheduler_tasks_on_startup import add_startup_scheduler_jobs
from app.bot.handlers.menu_commands import menu_commands_router
from app.bot.handlers.others import others_router

from config.config import Config

logger = logging.getLogger(__name__)


async def main(config: Config) -> None:
    logger.info("Starting bot...")

    # Initialising bot and dispatcher
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Including routers in order
    logger.info("Including Routers...")
    dp.include_routers(
        menu_commands_router,
        others_router,
    )

    # Cleaning alarms table
    logger.debug("Deleting due and marked for deletion alarms...")
    await delete_due_alarms()
    await hard_delete_soft_deleted_alarms()

    # Adding jobs to scheduler
    add_startup_scheduler_jobs()

    # Starting scheduler
    scheduler.start()
    logger.debug('Scheduler started...')

    # Starting polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
