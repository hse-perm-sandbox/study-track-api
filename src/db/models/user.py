from sqlalchemy.orm import Mapped

from src.db.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    name: Mapped[str]
    age: Mapped[int]
