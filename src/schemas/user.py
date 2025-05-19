from typing import Optional
from pydantic import BaseModel, model_validator

from src.schemas.base_dto import BaseDto


class UserBase(BaseModel):
    """Базовая схема пользователя"""

    name: str
    age: int
    


class UserDto(BaseDto, UserBase):
    """Базовая схема с ID и метками времени"""

    pass

class UserOptional(BaseModel):
    """Схема для частичного обновления пользователя"""

    name: Optional[str] = None
    age: Optional[int] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, data):
        if not (data.name or data.age):
            raise ValueError("Должно быть заполнено хотя бы одно из полей: name или age")
        return data