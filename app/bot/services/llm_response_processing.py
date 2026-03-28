from datetime import datetime
import logging

from app.infrastructure.database.queries import (
    create_one_time_alarm,
    create_recurring_alarm, )
from app.bot.services.cron_parsers import parse_cron_from_string
from app.infrastructure.database.models import Alarm

logger = logging.getLogger(__name__)


def _form_set_alarms_response(alarms_list: list[Alarm]) -> str:
    logger.debug(f'Forming set alarms response...')
    response_str = 'Created alarms:\n'
    for alarm in alarms_list:
        if alarm.date_time is not None:
            response_str += f'One time alarm at {alarm.date_time}\n'
        if alarm.cron is not None:
            response_str += f'Repeated alarm: {alarm.cron}\n'  # TODO добавить обработку для читаемости ответа
    return response_str


async def _process_set_alarms(
        chat_id: int,
        date_times: list[datetime] | None,
        crons: list[str] | None
) -> str:
    logger.debug('Processing user query for setting alarms...')
    new_alarms_list: list[Alarm] = []
    if len(date_times) > 0:
        for date_time in date_times:
            alarm = await create_one_time_alarm(chat_id=chat_id, date_time=date_time)
            new_alarms_list.append(alarm)
    if len(crons) > 0:
        for cron in crons:
            alarm = await create_recurring_alarm(chat_id=chat_id, cron=parse_cron_from_string(cron))
            new_alarms_list.append(alarm)
    return _form_set_alarms_response(new_alarms_list)


async def _process_edit_alarms() -> str:
    logger.debug('Processing user query for editing alarms...')
    # TODO complete function
    return 'Process edit alarms stub'


async def _process_delete_alarms() -> str:
    # TODO complete function
    logger.debug('Processing user query for deleting alarms...')
    return 'Process delete alarms stub'


def _process_invalid() -> str:
    logger.debug('Processing user query for invalid alarms...')
    return 'Invalid query, please try again'


async def process_llm_response(response: dict, chat_id: int) -> str:
    logger.debug(f'Processing LLM response:\n{response}')
    match response['query_type']:
        case 'set_alarms':
            return await _process_set_alarms(chat_id, response['date_times'], response['crons'])
        case 'edit_alarms':
            return await _process_edit_alarms()
        case 'delete_alarms':
            return await _process_delete_alarms()
        case 'invalid':
            return _process_invalid()
        case _:
            logger.error(f'Invalid query type: {response["query_type"]}')
            return 'We have experienced unexpected error, please try again'
