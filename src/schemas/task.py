from typing import Optional
from datetime import datetime
from pydantic import BaseModel, model_validator

from src.schemas.base_dto import BaseDto


class TaskBase(BaseModel):
    """Базовая схема задачи"""

    title: str
    description: str
    priority: str
    deadline: datetime
    category_id: int


class TaskDto(BaseDto, TaskBase):
    """Схема задачи с ID и временными метками"""

    user_id: int


class TaskOptional(BaseModel):
    """Схема для частичного обновления задачи"""

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, data):
        if not any([
            data.title,
            data.description,
            data.priority,
            data.deadline,
            data.category_id,
        ]):
            raise ValueError("Необходимо указать хотя бы одно поле для обновления")
        return data
