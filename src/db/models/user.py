from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.db.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String)

    #связь с задачами 
    tasks = relationship("Task", back_populates="user")
