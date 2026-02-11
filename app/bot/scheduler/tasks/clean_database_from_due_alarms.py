import logging

from app.bot.scheduler.scheduler import scheduler
from app.bot.scheduler.tasks.add_active_jobs_logging import add_active_jobs_logging

from config.config import load_config
from logging import getLogger

logger = getLogger(__name__)
config = load_config()


def clean_database_from_due_alarms():
    logger.debug('Cleaning database from due alarms')
    # TODO Add code to clean db from due alarms
