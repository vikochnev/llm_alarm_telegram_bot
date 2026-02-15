from aiogram import Bot

from config.config import load_config

import logging

logger = logging.getLogger(__name__)
config = load_config()


async def send_alarm_message(bot: Bot, chat_id: int):
    logger.debug(f"Sending user {chat_id} alarm message")
    await bot.send_message(chat_id=chat_id, text="Alarm! Time's up! ⏰")
