from datetime import timezone

from app.infrastructure.data_classes.data_classes import UserClass, AlarmClass
from app.bot.services.database_parsers import get_user_table, get_alarms_table

users_cache: list[UserClass] = []
alarms_cache: list[AlarmClass] = []

async def update_user_cache() -> None:
    users = await get_user_table()
    users_cache.clear()
    for user in users:
        users_cache.append(
            UserClass(
                chat_id=user.chat_id,
                timezone=user.timezone,
                language=user.language,
            )
        )


async def update_alarm_cache() -> None:
    alarms = await get_alarms_table()
    alarms_cache.clear()
    for alarm in alarms:
        alarms_cache.append(
            AlarmClass(
                alarm_id=alarm.alarm_id,
                chat_id=alarm.chat_id,
                is_repeated=alarm.is_repeated,
                date_time=alarm.date_time,
                cron=alarm.cron,
            )
        )

def get_user_from_cache(chat_id: int) -> UserClass:
    return next((user for user in users_cache if user.chat_id == chat_id), None)

def get_alarms_from_cache(chat_id: int) -> list[AlarmClass]:
    return [alarm for alarm in alarms_cache if alarm.chat_id == chat_id]