from pydantic import BaseModel, Field
from typing import Literal, Dict
from datetime import datetime


class Settings(BaseModel):
    timezone: int | str | None
    language: Literal['ru', 'en'] = 'ru'


class CronSettings(BaseModel):
    minute: int | str
    hour: int | str
    day_of_week: int | str = '*'
    month: int | str = '*'


class Alarm(BaseModel):
    alarm_id: int = Field(gt=0)
    is_repeated: bool = False
    datetime: datetime
    cron: CronSettings | None
    active: bool = True


class User(BaseModel):
    chat_id: int = Field(gt=0)
    user_settings: Settings
    alarms: list[Alarm]


class Database(BaseModel):
    users: list[User] | None


db: Database = []
