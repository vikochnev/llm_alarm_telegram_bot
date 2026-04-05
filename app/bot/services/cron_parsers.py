from cron_validator import CronValidator

from app.infrastructure.data_classes.data_classes import CronSettings

from logging import getLogger

logger = getLogger(__name__)


def parse_cron_to_string(cron: CronSettings):
    logger.debug(f'Parsing cron settings to string: {cron}')
    cron_string = f'{cron.minute} {cron.hour} {cron.day_of_month} {cron.month} {cron.day_of_week}'
    return cron_string


def parse_cron_from_string(cron_string: str):
    logger.debug(f'Parsing cron settings from string: {cron_string}')
    try:
        assert CronValidator.parse(cron_string)
        cron_list = cron_string.split()
        cron = CronSettings()
        cron.minute = cron_list[0]
        cron.hour = cron_list[1]
        cron.day_of_month = cron_list[2]
        cron.month = cron_list[3]
        cron.day_of_week = cron_list[4]
        return cron
    except ValueError as e:
        logger.error(f'Could not parse cron settings from string to CronSettings: {e}')