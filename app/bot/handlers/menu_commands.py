import logging
from datetime import datetime, timezone

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from app.bot.services.local_memory.functions import get_user_from_cache
from app.infrastructure.database.queries import create_user

logger = logging.getLogger(__name__)

# Инициализируем роутер
menu_commands_router = Router()


# Этот хендлер будет срабатывать на любые апдейты типа Message, не забранные другими хэндлерами
@menu_commands_router.message(CommandStart())
async def process_start_command(message: Message):
    logger.debug('Processing processing /start command...')
    if not get_user_from_cache(message.chat.id):
        logger.debug(f'Registering user with id: {message.chat.id}...')
        await create_user(
            chat_id=message.chat.id,
            timezone='Europe/Moscow',  # TODO Add functional to choose/change timezone
            language='English',  # TODO add functional to choose/change user language
            )

    await message.answer(text="This is an alarm setting bot,\n"
                              "Please tell me when to set your alarms")
