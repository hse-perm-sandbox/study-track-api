from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.category import Category
from src.db.repositories.base import BaseRepository
from src.schemas.category import CategoryDto, CategoryOptional


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    async def get_all(self, db: AsyncSession) -> List[CategoryDto]:
        categories = await super().get_all(db)
        return [CategoryDto.model_validate(category) for category in categories]

    async def get_all_by_user(self, db: AsyncSession, user_id: int) -> List[CategoryDto]:
        stmt = select(Category).where(Category.user_id == user_id)
        result = await db.execute(stmt)
        categories = result.scalars().all()
        return [CategoryDto.model_validate(category) for category in categories]

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> Optional[CategoryDto]:
        category = await super().get_by_id(db, obj_id)
        return CategoryDto.model_validate(category) if category else None

    async def add(self, db: AsyncSession, obj: Category) -> CategoryDto:
        category = await super().add(db, obj)
        return CategoryDto.model_validate(category)

    async def update(
        self, db: AsyncSession, obj_id: int, category_data: CategoryOptional
    ) -> CategoryDto:
        category = await super().get_by_id(db, obj_id)
        if not category:
            raise ValueError(f"Категория с ID {obj_id} не найдена")
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        await db.commit()
        await db.refresh(category)
        return CategoryDto.model_validate(category)

    async def delete(self, db: AsyncSession, category_dto: CategoryDto) -> None:
        result = await db.execute(select(Category).where(Category.id == category_dto.id))
        category = result.scalar_one_or_none()
        if category:
            await super().delete(db, category)
