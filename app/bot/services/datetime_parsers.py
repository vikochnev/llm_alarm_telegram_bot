from datetime import datetime
import logging

from config.config import load_config

logger = logging.getLogger(__name__)

config = load_config()


def convert_str_to_datetime(dt_str: str) -> datetime:
    logger.debug(f"Formatting string: '{dt_str}' to datetime format")
    return datetime.strptime(dt_str, config.const.datetime_format)
