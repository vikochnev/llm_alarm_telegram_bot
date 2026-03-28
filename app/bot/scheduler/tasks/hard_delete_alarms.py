from app.bot.scheduler.scheduler import scheduler
from app.bot.services.database_parsers import hard_delete_soft_deleted_alarms
from logging import getLogger
from config.config import load_config

logger = getLogger(__name__)
config = load_config()

def add_hard_delete_alarms_job():
    logger.debug('Adding job which hard deletes alarms marked as soft deleted...')
    scheduler.add_job(func=hard_delete_soft_deleted_alarms,
                      trigger='interval',
                      minutes=config.const.scheduler_hard_delete_alarms_interval_m,
                      id='hard_delete_alarms')