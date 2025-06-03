from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]

    tasks = relationship("Task", back_populates="category")
    user = relationship("User", back_populates="categories")
