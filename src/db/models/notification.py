from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import BaseModel

class Notification(BaseModel):
    __tablename__ = "notifications"

    task_id = Mapped[int]
    time_notification = Mapped[datetime]
    type = Mapped[str]