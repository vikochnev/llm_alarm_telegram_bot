from aiogram import Bot

from datetime import datetime
import asyncio

from app.bot.services.send_scheduled_message import send_alarm_message

from infrastructure.database.database import alarms

from config.config import load_config


import logging

logger = logging.getLogger(__name__)
config = load_config()


async def alarm_checker(bot: Bot):
    logger.info("Starting alarm checking coroutine...")
    while True:
        now = datetime.now()
        for chat_id, alarms_list in list(alarms.items()):
            if not alarms_list:
                continue
            due_alarms = [dt for dt in alarms_list if abs((dt - now).total_seconds() <= config.const.sleep_interval)]
            for due_time in due_alarms:
                await send_alarm_message(bot=bot, chat_id=chat_id)
                logger.debug(f"Deleting sent alarm from db from user {chat_id}")
                alarms_list.remove(due_time)

            if not alarms_list:
                logger.debug(f"Deleting user {chat_id} from db due to having no active alarms")
                del alarms[chat_id]

        logger.debug(f"Alarm coroutine live cached db: {alarms}")
        await asyncio.sleep(config.const.sleep_interval)
