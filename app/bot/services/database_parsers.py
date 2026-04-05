from datetime import datetime, timezone, timedelta
from sqlalchemy import select
import logging

from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.database.core import async_session_maker
from app.infrastructure.database.models import User, Alarm
from app.infrastructure.database.queries import delete_alarm

from config.config import load_config
config = load_config()
logger = logging.getLogger(__name__)

async def get_user_table():
    logger.debug(f'Getting user table from DB')
    async with async_session_maker() as session:
        try:
            stmt = select(User)
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(e)

async def get_alarms_table():
    logger.debug(f'Getting alarms table from DB')
    async with async_session_maker() as session:
        try:
            stmt = select(Alarm)
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(e)

async def delete_due_alarms():
    logger.debug(f'Deleting due alarms from DB')
    async with async_session_maker() as session:
        try:
            stmt = select(Alarm).where(Alarm.date_time < datetime.now(timezone.utc))
            result = await session.execute(stmt)
            alarms = result.scalars().all()
            for alarm in alarms:
                await delete_alarm(alarm_id=alarm.alarm_id)
        except SQLAlchemyError as e:
            logger.error(e)

async def hard_delete_soft_deleted_alarms():
    logger.debug(f'Hard deleting soft deleted alarms from DB')
    async with async_session_maker() as session:
        try:
            stmt = select(Alarm).where(Alarm.deleted_at.is_not(None))
            result = await session.execute(stmt)
            alarms = result.scalars().all()
            for alarm in alarms:
                if alarm.date_time < (datetime.now(timezone.utc) - timedelta(hours=config.const.timeout_delete_hours)):
                    await delete_alarm(alarm_id=alarm.alarm_id)
        except SQLAlchemyError as e:
            logger.error(e)
