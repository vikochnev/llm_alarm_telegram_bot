import json
import logging

from aiogram import Router
from aiogram.types import Message

from app.bot.llm.llm_queries import get_general_llm_response
from app.bot.services.parse_datetime import convert_str_to_datetime
from infrastructure.database.database import alarms

logger = logging.getLogger(__name__)

# Инициализируем роутер
others_router = Router()


# Этот хендлер будет срабатывать на любые апдейты типа Message, не забранные другими хэндлерами
@others_router.message()
async def send_echo(message: Message):
    logger.debug(f"Processing message from user id {message.from_user.id}")
    response_str = await get_general_llm_response(user_input=message.text)
    response = json.loads(response_str)
    if 'date_time' not in response.keys():
        logger.debug(f"LLM determined user message was without alarm timers")
    else:
        user_id = message.from_user.id
        if user_id not in alarms.keys():
            logger.debug("Creating new user profile")
            alarms[user_id] = [convert_str_to_datetime(response['date_time'])]
        else:
            logger.debug("Adding new alarms to user")
            alarms[user_id].append(convert_str_to_datetime(response['date_time']))
    logger.debug("Sending user answer from LLM")
    await message.answer(response['answer'])
