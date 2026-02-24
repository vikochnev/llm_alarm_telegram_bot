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
class OrmSettings:
    base_url: str


@dataclass
class ConstSettings:
    sleep_interval: int
    datetime_format: str


@dataclass
class Config:
    bot: BotSettings
    llm: LlmSettings
    # db: DatabaseSettings
    redis: RedisSettings
    log: LoggerSettings
    orm: OrmSettings
    const: ConstSettings


def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(f".env file not found at {path}, skipping...")
        else:
            logger.info(f"loading .env from {path}")

    env.read_env(path)

    bot_settings = BotSettings(
        token=env.str("BOT_TOKEN"),
    )

    llm_settings = LlmSettings(
        token=env.str("LLM_API_TOKEN"),
        model=env.str("LLM_MODEL"),
        base_url=env.str("LLM_BASE_URL"),
    )

    redis_settings = RedisSettings(
        host=env.str("REDIS_HOST"),
        port=env.str("REDIS_PORT"),
        db=env.int("REDIS_DATABASE"),
        username=env.str("REDIS_USERNAME"),
        password=env.str("REDIS_PASSWORD"),
    )

    orm_settings = OrmSettings(
        base_url=env.str("ORM_BASE_URL"),
    )

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
        bot=bot_settings,
        llm=llm_settings,
        log=logger_settings,
        orm=orm_settings,
        const=const_settings,
    )
