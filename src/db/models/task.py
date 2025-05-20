from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]
    description: Mapped[str]
    priority: Mapped[str]  
    deadline: Mapped[datetime]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))