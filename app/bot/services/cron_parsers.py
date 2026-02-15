from cron_validator import CronValidator

from app.infrastructure.data_classes.data_classes import CronSettings

from logging import getLogger

logger = getLogger(__name__)


def parse_cron_to_string(cron: CronSettings):
    cron_string = f'{cron.minute} {cron.hour} {cron.day_of_month} {cron.month} {cron.day_of_week}'
    return cron_string


def parse_cron_from_string(cron_string: str):
    try:
        assert CronValidator.parse(cron_string)
        cron = CronSettings()
        cron.minute = cron_string[0]
        cron.hour = cron_string[1]
        cron.day_of_month = cron_string[2]
        cron.month = cron_string[3]
        cron.day_of_week = cron_string[4]
        return cron
    except ValueError as e:
        logger.error(f'Could not parse cron settings from string to CronSettings: {e}')