from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.core import Base


class Alarm(Base):
    __tablename__ = "alarms"

    alarm_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('users.chat_id'), nullable=False)
    is_repeated = Column(Boolean, default=False, nullable=False)
    date_time = Column(DateTime(timezone=True), index=True, nullable=True)
    cron = Column(String, index = True, nullable = True)

class User(Base):
    __tablename__ = "users"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timezone = Column(String, nullable=False)
    language = Column(String, nullable=False)
