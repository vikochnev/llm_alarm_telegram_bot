from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from pydantic import BaseModel
from typing import Literal

from app.infrastructure.database.core import Base


class UserSettings(BaseModel):
    timezone: int | str | None
    language: Literal['ru', 'en'] = 'ru'


class CronSettings(BaseModel):
    minute: int | str
    hour: int | str
    day_of_month: int | str = '*'
    month: int | str = '*'
    day_of_week: int | str = '*'


class Alarm(Base):
    __tablename__ = "alarms"

    alarm_id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('users.chat_id'), nullable=False)
    is_repeated = Column(Boolean, default=False, nullable=False)
    datetime = Column(DateTime, index=True, nullable=True)
    cron = Column(String, index = True, nullable = True)

class User(Base):
    __tablename__ = "users"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
