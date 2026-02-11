from app.bot.scheduler.scheduler import scheduler
from logging import getLogger
from config.config import load_config

logger = getLogger(__name__)
config = load_config()

def _log_active_jobs():
    logger.info(scheduler.get_active_jobs())


def add_active_jobs_logging():
    logger.debug('Starting logging of scheduled jobs...')
    scheduler.add_job(func=_log_active_jobs(),
                      trigger='interval',
                      seconds=config.const.sleep_interval,
                      id='log_active_jobs')
