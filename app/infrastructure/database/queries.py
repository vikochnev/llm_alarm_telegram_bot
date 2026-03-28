from sqlalchemy import select
from sqlalchemy.orm import joinedload

from datetime import datetime

from app.infrastructure.database.core import async_session_maker
from app.infrastructure.database.models import User, Alarm
from app.infrastructure.data_classes.data_classes import CronSettings
from app.bot.services.cron_parsers import parse_cron_to_string

from logging import Logger

logger = Logger(__name__)



async def create_user(*, chat_id: int, timezone: str, language: str) -> User:
    async with async_session_maker() as session:
        user = User(
            chat_id=chat_id,
            timezone=timezone,
            language=language)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.debug(f"User created: {user}")
        return user


async def create_one_time_alarm(*, chat_id: int, date_time: datetime) -> Alarm:
    async with async_session_maker() as session:
        alarm = Alarm(
            chat_id=chat_id,
            is_repeated=False,
            date_time=date_time,
            cron=None,
        )
        session.add(alarm)
        await session.commit()
        await session.refresh(alarm)
        logger.debug(f"Alarm created: {alarm}")
        return alarm


async def create_recurring_alarm(*, chat_id: int, cron: CronSettings) -> Alarm:
    async with async_session_maker() as session:
        cron_string = parse_cron_to_string(cron)
        alarm = Alarm(
            chat_id=chat_id,
            is_repeated=True,
            date_time=None,
            cron=cron_string,
        )
        session.add(alarm)
        await session.commit()
        await session.refresh(alarm)
        logger.debug(f"Alarm created: {alarm}")
        return alarm


async def delete_alarm(*, alarm_id: int) -> None:
    async with async_session_maker() as session:
        try:
            alarm = await session.get(Alarm, alarm_id)
            await session.delete(alarm)
            await session.commit()
        except:
            logger.debug(f"Alarm with id {alarm_id} was not found")
