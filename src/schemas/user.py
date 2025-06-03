from typing import Optional

from pydantic import BaseModel, model_validator

from src.schemas.base_dto import BaseDto


class UserBase(BaseModel):
    """Базовая схема пользователя"""

    name: str
    email: str
    password: str


class UserDto(BaseDto):
    """Базовая схема с ID и метками времени"""

    name: str
    email: str


class UserOptional(BaseModel):
    """Схема для частичного обновления пользователя"""

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, data):
        if not (data.name or data.email or data.password):
            raise ValueError(
                "Должно быть заполнено хотя бы одно из полей: name, email или password"
            )
        return data
