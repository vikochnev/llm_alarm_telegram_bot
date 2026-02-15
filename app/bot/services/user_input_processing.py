from app.bot.services.datetime_parsers import convert_str_to_datetime

import logging

logger = logging.getLogger(__name__)


async def process_llm_response(response: dict, chat_id: int) -> str:
    logger.debug(f'Processing LLM response:\n{response}')
    pass
