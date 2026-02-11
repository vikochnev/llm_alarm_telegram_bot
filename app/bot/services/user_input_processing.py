from app.bot.services.parse_datetime import convert_str_to_datetime
from app.infrastructure.database.database import db

import logging

logger = logging.getLogger(__name__)


async def process_llm_response(response: dict, chat_id: int) -> str:
    logger.debug(f'Processing LLM response:\n{response}')
    pass
