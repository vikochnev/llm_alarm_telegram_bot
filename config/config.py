import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)

# config constants
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMEOUT_DELETE_HOURS: int = 6
SCHEDULER_DELETE_DUE_ALARMS_INTERVAL_M: int = 60
SCHEDULER_HARD_DELETE_ALARMS_INTERVAL_M: int = 60
SCHEDULER_UPDATE_LOCAL_MEMORY_INTERVAL_S: int = 60
SCHEDULER_JOB_LOGGING_INTERVAL_S: int = 60


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


# @dataclass
# class RedisSettings:
#     host: str
#     port: str
#     db: int
#     password: str
#     username: str
#     default_ttl: int


@dataclass
class LoggerSettings:
    level: str
    format: str


@dataclass
class OrmSettings:
    base_url: str


@dataclass
class ConstSettings:
    datetime_format: str
    timeout_delete_hours: int
    scheduler_delete_due_alarms_interval_m: int
    scheduler_hard_delete_alarms_interval_m: int
    scheduler_update_local_memory_interval_s: int
    scheduler_job_logging_interval_s: int


@dataclass
class Config:
    bot: BotSettings
    llm: LlmSettings
    db: DatabaseSettings
    # redis: RedisSettings
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

    db_settings = DatabaseSettings(
        name=env.str('POSTGRES_DB'),
        host=env.str('POSTGRES_HOST'),
        port=env.str('POSTGRES_PORT'),
        user=env.str('POSTGRES_USER'),
        password=env.str('POSTGRES_PASSWORD'),
    )

    # redis_settings = RedisSettings(
    #     host=env.str("REDIS_HOST"),
    #     port=env.str("REDIS_PORT"),
    #     db=env.int("REDIS_DATABASE"),
    #     username=env.str("REDIS_USERNAME"),
    #     password=env.str("REDIS_PASSWORD"),
    #     default_ttl=REDIS_DEFAULT_TTL,
    # )

    orm_settings = OrmSettings(
        base_url=f'postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/alarms_bot_db',
    )

    logger_settings = LoggerSettings(
        level=env.str("LOG_LEVEL"),
        format=env.str("LOG_FORMAT"),
    )

    const_settings = ConstSettings(
        datetime_format=DATETIME_FORMAT,
        timeout_delete_hours=TIMEOUT_DELETE_HOURS,
        scheduler_delete_due_alarms_interval_m=SCHEDULER_DELETE_DUE_ALARMS_INTERVAL_M,
        scheduler_hard_delete_alarms_interval_m=SCHEDULER_HARD_DELETE_ALARMS_INTERVAL_M,
        scheduler_update_local_memory_interval_s=SCHEDULER_UPDATE_LOCAL_MEMORY_INTERVAL_S,
        scheduler_job_logging_interval_s=SCHEDULER_JOB_LOGGING_INTERVAL_S,
    )

    logger.info("Configuration loaded successfully")

    return Config(
        bot=bot_settings,
        llm=llm_settings,
        log=logger_settings,
        db=db_settings,
        # redis=redis_settings,
        orm=orm_settings,
        const=const_settings,
    )
