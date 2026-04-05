from app.bot.scheduler.scheduler import scheduler
from app.bot.services.local_memory.functions import update_user_cache, update_alarm_cache
from logging import getLogger
from config.config import load_config

logger = getLogger(__name__)
config = load_config()

def add_update_local_memory_users_job():
    logger.debug('Adding job which updates local memory users variable...')
    scheduler.add_job(func=update_user_cache(),
                      trigger='interval',
                      seconds=config.const.scheduler_update_local_memory_interval_s,
                      id='update_local_memory_users')

def add_update_local_memory_alarms_job():
    logger.debug('Adding job which updates local memory alarms variable...')
    scheduler.add_job(func=update_alarm_cache(),
                      trigger='interval',
                      seconds=config.const.scheduler_update_local_memory_interval_s,
                      id='update_local_memory_alarms')