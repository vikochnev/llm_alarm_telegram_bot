from pydantic import BaseModel
from typing import Literal
from datetime import datetime
class UserSettings(BaseModel):
    timezone: str  # For storing as IANA name
    language: Literal['ru', 'en'] = 'ru'


class CronSettings(BaseModel):
    minute: int | str = '*'
    hour: int | str = '*'
    day_of_month: int | str = '*'
    month: int | str = '*'
    day_of_week: int | str = '*'


class AlarmJoinedOnUser(BaseModel):
    alarm_id: int
    chat_id: int
    user_settings: UserSettings
    is_repeated: bool
    datetime: datetime | None
    cron: CronSettings | None
