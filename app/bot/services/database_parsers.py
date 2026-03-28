from datetime import datetime, timezone, timedelta
from sqlalchemy import select

from app.infrastructure.database.core import async_session_maker
from app.infrastructure.database.models import User, Alarm
from app.infrastructure.database.queries import delete_alarm

from config.config import load_config
config = load_config()

async def get_user_table():
    async with async_session_maker() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_alarms_table():
    async with async_session_maker() as session:
        stmt = select(Alarm)
        result = await session.execute(stmt)
        return result.scalars().all()

async def delete_due_alarms():
    async with async_session_maker() as session:
        stmt = select(Alarm).where(Alarm.date_time < datetime.now(timezone.utc))
        result = await session.execute(stmt)
        alarms = result.scalars().all()
        for alarm in alarms:
            await delete_alarm(alarm_id=alarm.alarm_id)

async def hard_delete_soft_deleted_alarms():
    async with async_session_maker() as session:
        stmt = select(Alarm).where(Alarm.deleted_at.is_not(None))
        result = await session.execute(stmt)
        alarms = result.scalars().all()
        for alarm in alarms:
            if alarm.date_time < (datetime.now(timezone.utc) - timedelta(hours=config.const.timeout_delete_hours)):
                await delete_alarm(alarm_id=alarm.alarm_id)


