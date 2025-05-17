from typing import Optional
from pydantic import BaseModel, field_validator

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

    @field_validator("name", "age", mode="after")
    def at_least_one_field(cls, v, values):
        if not (values.get("name") or values.get("age")):
            raise ValueError("Должно быть заполнено хотя бы одно из полей: name или age")
        return v