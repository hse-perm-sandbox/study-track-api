from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User
from src.db.repositories.base import BaseRepository
from src.schemas.user import UserDto, UserOptional

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_all(self, db: AsyncSession) -> List[UserDto]:
        users = await super().get_all(db)
        return [UserDto.model_validate(user) for user in users]

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> Optional[UserDto]:
        user = await super().get_by_id(db, obj_id)
        return UserDto.model_validate(user) if user else None

    async def add(self, db: AsyncSession, obj: User) -> UserDto:
        user = await super().add(db, obj)
        return UserDto.model_validate(user)

    async def update(self, db: AsyncSession, obj_id: int, user_data: UserOptional) -> UserDto:
        user = await super().get_by_id(db, obj_id)
        if not user:
            raise ValueError(f"Пользователь с ID {obj_id} не найден")
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await db.commit()
        await db.refresh(user)
        return UserDto.model_validate(user)
    

    async def delete(self, db: AsyncSession, user_dto: UserDto) -> None:
        result = await db.execute(select(User).where(User.id == user_dto.id))
        user = result.scalar_one_or_none()
        if user:
            await super().delete(db, user)