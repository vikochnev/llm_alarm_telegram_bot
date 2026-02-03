from app.bot.services.parse_datetime import convert_str_to_datetime
from app.infrastructure.database.database import alarms

import logging

logger = logging.getLogger(__name__)


async def process_llm_response(response: dict, chat_id: int) -> str:
    logger.debug(f'Processing LLM response:\n{response}')
    if 'query_type' not in response.keys():
        return response["answer"]
    match response["query_type"]:
        case "set_alarms":
            if chat_id not in alarms.keys():
                alarms[chat_id] = []
            for datetime in response["date_times"]:
                alarms[chat_id].append(convert_str_to_datetime(datetime))
            answer = response["answer"]
        case "edit_alarms":
            if not chat_id in alarms.keys() or not alarms[chat_id]:
                answer = "You don't have active alarms to edit"
            else:
                answer = "TODO: add edit_alarms"
        case "delete_alarms":
            if not chat_id in alarms.keys() or not alarms[chat_id]:
                answer = "You don't have active alarms to delete"
            else:
                answer = "TODO: add delete_alarms"
        case _:
            # TODO добавить нормальный обработчик ошибок
            answer = "I have experienced unexpected error :("
    return answer
