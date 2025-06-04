from typing import Optional

from pydantic import BaseModel, model_validator

from src.schemas.base_dto import BaseDto


class CategoryBase(BaseModel):
    """Базовая схема категории"""
    name: str
    user_id: int


class CategoryDto(BaseDto):
    """Схема категории с ID и метками времени"""
    name: str
    user_id: int


class CategoryOptional(BaseModel):
    """Схема для частичного обновления категории"""
    name: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, data):
        if data.name is None:
            raise ValueError("Необходимо указать хотя бы одно поле для обновления")
        return data