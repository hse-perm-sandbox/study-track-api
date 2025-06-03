from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    time_notification = Mapped[datetime]
    type = Mapped[str]

    task = relationship("Task", back_populates="notifications")
