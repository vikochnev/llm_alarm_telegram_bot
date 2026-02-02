import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart

logger = logging.getLogger(__name__)

# Инициализируем роутер
menu_commands_router = Router()


# Этот хендлер будет срабатывать на любые апдейты типа Message, не забранные другими хэндлерами
@menu_commands_router.message(CommandStart())
async def process_start_command(message: Message):
    logger.debug('Started processing /start command')
    await message.answer(text="This is an alarm setting bot,\n"
                              "Please tell me when to set your alarms")
    logger.debug('Awaited /start command answer')
