from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class UserSettings(BaseModel):
    timezone: str  # For storing as IANA name
    language: Literal['Russian', 'English'] = 'Russian'


class CronSettings(BaseModel):
    minute: int | str = '*'
    hour: int | str = '*'
    day_of_month: int | str = '*'
    month: int | str = '*'
    day_of_week: int | str = '*'


class UserClass(BaseModel):
    chat_id: int
    timezone: str
    language: str


class AlarmClass(BaseModel):
    alarm_id: int
    chat_id: int
    is_repeated: bool
    date_time: datetime | None
    cron: str | None
