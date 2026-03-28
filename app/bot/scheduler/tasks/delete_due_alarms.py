from app.bot.scheduler.scheduler import scheduler
from app.bot.services.database_parsers import delete_due_alarms
from logging import getLogger
from config.config import load_config

logger = getLogger(__name__)
config = load_config()

def add_delete_due_alarms_job():
    logger.debug('Adding job which deletes due alarms...')
    scheduler.add_job(func=delete_due_alarms,
                      trigger='interval',
                      minutes=config.const.scheduler_delete_due_alarms_interval_m,
                      id='delete_due_alarms')