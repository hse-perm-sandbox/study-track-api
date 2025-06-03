from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import BaseModel


class Task(BaseModel):  # наследуемся от base.py
    __tablename__ = "tasks"  # создаем таблице название

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )  # внешний ключ ссылающийся на таблицу users (колонка id)
    title: Mapped[str]  # задали тип строка
    description: Mapped[str]  # задали тип строка
    priority: Mapped[str]  # задали тип строка
    deadline: Mapped[datetime]  # задали тип дата время
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )  # внешний ключ ссылающийся на таблицу categories (колонка id)

    notifications = relationship("Notification", back_populates="task")
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
