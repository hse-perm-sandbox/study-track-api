from datetime import datetime                                  #импортируем тип данных "дата время"
from sqlalchemy import ForeignKey, String, Integer, Date       #импортируем остальные типы данных  
from sqlalchemy.orm import Mapped, mapped_column, relationship #это для задачи типа данных полей, последний для связи с другими моделями

from src.db.models.base import BaseModel                       #для наследования


class Task(BaseModel):       #наследуемся от base.py
    __tablename__ = "tasks"  #создаем таблице название

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))          #внешний ключ ссылающийся на таблицу users (колонка id)
    title: Mapped[str]                                                    #задали тип строка
    description: Mapped[str]                                              #задали тип строка
    priority: Mapped[str]                                                 #задали тип строка
    deadline: Mapped[datetime]                                            #задали тип дата время
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id")) #внешний ключ ссылающийся на таблицу categories (колонка id)

    notifications = relationship("Notification", back_populates="task")   #задаем связь с таблицей Notification
                                                                          #*тут не уверен правильно ли написал связь