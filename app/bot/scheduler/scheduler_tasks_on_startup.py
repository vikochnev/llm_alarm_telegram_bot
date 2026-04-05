from app.bot.scheduler.tasks.delete_due_alarms import add_delete_due_alarms_job
from app.bot.scheduler.tasks.hard_delete_alarms import add_hard_delete_alarms_job
from app.bot.scheduler.tasks.update_local_memory import update_user_cache, update_alarm_cache
from app.bot.scheduler.tasks.add_active_jobs_logging import add_active_jobs_logging

import logging

logger = logging.getLogger(__name__)

def add_startup_scheduler_jobs():
    logger.debug("Adding startup scheduler jobs...")
    add_active_jobs_logging()
    update_user_cache()
    update_alarm_cache()
    add_delete_due_alarms_job()
    add_hard_delete_alarms_job()
    add_active_jobs_logging()
