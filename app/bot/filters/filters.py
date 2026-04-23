from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from psycopg import AsyncConnection
from app.bot.services.local_memory.functions import get_user_from_cache
from app.infrastructure.data_classes.data_classes import UserClass


class UserInDBFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return get_user_from_cache(chat_id=event.from_user.id) is not None


