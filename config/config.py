import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str


@dataclass
class LlmSettings:
    token: str
    model: str
    base_url: str


@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: str
    user: str
    password: str


@dataclass
class RedisSettings:
    host: str
    port: str
    db: int
    password: str
    username: str


@dataclass
class LoggerSettings:
    level: str
    format: str


@dataclass
class ConstSettings:
    sleep_interval: int
    datetime_format: str


@dataclass
class Config:
    bot: BotSettings
    llm: LlmSettings
    #db: DatabaseSettings
    #redis: RedisSettings
    log: LoggerSettings
    const: ConstSettings


def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(f".env file not found at {path}, skipping...")
        else:
            logger.info(f"loading .env from {path}")

    env.read_env(path)

    bot_token = env("BOT_TOKEN")

    if not bot_token:
        raise ValueError("BOT_TOKEN must not be empty")

    llm_token = env("LLM_API_TOKEN")

    if not llm_token:
        raise ValueError("LLM_API_TOKEN must not be empty")

    llm_model = env("LLM_MODEL")

    if not llm_model:
        raise ValueError("LLM_MODEL must not be empty")

    llm_base_url = env("LLM_BASE_URL")

    if not llm_base_url:  # Проверить необходимость параметра для запуска лмм
        raise ValueError("LLM_BASE_URL must not be empty")

    logger_settings = LoggerSettings(
        level=env.str("LOG_LEVEL"),
        format=env.str("LOG_FORMAT"),
    )

    const_settings = ConstSettings(
        sleep_interval=env.int("SLEEP_INTERVAL"),
        datetime_format=env.str("DATETIME_FORMAT"),
    )

    logger.info("Configuration loaded successfully")

    return Config(
        bot=BotSettings(token=bot_token),
        llm=LlmSettings(token=llm_token, model=llm_model, base_url=llm_base_url),
        log=logger_settings,
        const=const_settings,
    )
