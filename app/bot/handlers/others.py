import json
import logging

from aiogram import Router
from aiogram.types import Message

from app.bot.llm.llm_queries import get_general_llm_response
from app.bot.services.llm_response_processing import process_llm_response
from app.bot.services.local_memory.functions import get_user_from_cache

logger = logging.getLogger(__name__)

# Инициализируем роутер
others_router = Router()


# Этот хендлер будет срабатывать на любые апдейты типа Message, не забранные другими хэндлерами
@others_router.message()
async def process_general_input(message: Message):
    logger.debug(f"Processing message from user id {message.from_user.id}")
    if not get_user_from_cache(message.from_user.id):
        answer = "User not registered, please, use /start command to start working with bot"
    else:
        response_str = await get_general_llm_response(user_input=message.text)
        await message.answer(response_str)
        response = json.loads(response_str)
        answer = await process_llm_response(response=response, chat_id=message.from_user.id)
    await message.answer(answer)
