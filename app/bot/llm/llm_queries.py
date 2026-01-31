from openai import OpenAI

from app.bot.llm.instructions import general_instructions_template

from datetime import datetime

from config.config import load_config
import logging

logger = logging.getLogger(__name__)

config = load_config()

# Инициализируем клиент чатбота
logger.info("Initialising LLM client...")
client = OpenAI(
    base_url=config.llm.base_url,
    api_key=config.llm.token,
)


async def get_general_llm_response(user_input):
    logger.debug("Sending user query to LLM")
    response = client.responses.create(
        model=config.llm.model,
        instructions=general_instructions_template.format(current_time=datetime.now()),
        input=user_input
    )
    return response.output_text
