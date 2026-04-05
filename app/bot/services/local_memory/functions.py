from app.infrastructure.data_classes.data_classes import UserClass, AlarmClass
from app.bot.services.database_parsers import get_user_table, get_alarms_table
from app.bot.services.local_memory.variables import users_cache, alarms_cache
from app.bot.services.cron_parsers import parse_cron_from_string
from app.infrastructure.database.queries import create_user, create_one_time_alarm, create_recurring_alarm
import logging

logger = logging.getLogger(__name__)


def _add_user_to_memory(user: UserClass) -> None:
    logger.debug(f'Registering user with id: {user.id}...')
    users_cache.append(
        UserClass(
            chat_id=user.chat_id,
            timezone=user.timezone,
            language=user.language,
        )
    )


def _add_alarm_to_memory(alarm: AlarmClass) -> None:
    logger.debug(f'Registering alarm with id: {alarm.id}...')
    alarms_cache.append(
        AlarmClass(
            alarm_id=alarm.alarm_id,
            chat_id=alarm.chat_id,
            is_repeated=alarm.is_repeated,
            date_time=alarm.date_time,
            cron=alarm.cron,
        )
    )


async def update_user_cache() -> None:
    logger.debug('Updating users cache...')
    users = await get_user_table()
    users_cache.clear()
    for user in users:
        _add_user_to_memory(user)


async def update_alarm_cache() -> None:
    logger.debug('Updating alarms cache...')
    alarms = await get_alarms_table()
    alarms_cache.clear()
    for alarm in alarms:
        _add_alarm_to_memory(alarm)


def get_user_from_cache(chat_id: int) -> UserClass:
    logger.debug(f'Getting user with id: {chat_id}...')
    return next((user for user in users_cache if user.chat_id == chat_id), None)


def get_alarms_from_cache(chat_id: int) -> list[AlarmClass]:
    logger.debug(f'Getting alarms with id: {chat_id}...')
    return [alarm for alarm in alarms_cache if alarm.chat_id == chat_id]


async def add_user_to_memory_and_db(user: UserClass) -> None:
    logger.debug(f'Registering user with id: {user.id}...')
    _add_user_to_memory(user)
    await create_user(chat_id=user.chat_id,
                      timezone=user.timezone,
                      language=user.language)


async def add_alarm_to_memory_and_db(alarm: AlarmClass) -> None:
    # TODO find out how to add autoincrement SQL alarm_id key without requesting DB, and if such approach is necessary
    logger.debug(f'Registering alarm with id: {alarm.id}...')
    _add_alarm_to_memory(alarm)
    if alarm.is_repeated:
        await create_recurring_alarm(chat_id=alarm.chat_id,
                                     cron=parse_cron_from_string(alarm.cron))
    else:
        await create_one_time_alarm(chat_id=alarm.chat_id,
                                    date_time=alarm.date_time, )
