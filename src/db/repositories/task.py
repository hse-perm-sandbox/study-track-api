from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.task import Task
from src.db.repositories.base import BaseRepository
from src.schemas.task import TaskDto, TaskBase, TaskOptional


class TaskRepository(BaseRepository[Task]):
    def __init__(self):
        super().__init__(Task)

    async def get_all_by_user(self, db: AsyncSession, user_id: int) -> List[TaskDto]:
        stmt = select(Task).where(Task.user_id == user_id)
        result = await db.execute(stmt)
        tasks = result.scalars().all()
        return [TaskDto.model_validate(task) for task in tasks]

    async def get_by_id(self, db: AsyncSession, task_id: int) -> Optional[TaskDto]:
        task = await super().get_by_id(db, task_id)
        return TaskDto.model_validate(task) if task else None

    async def add(self, db: AsyncSession, task: Task) -> TaskDto:
        task = await super().add(db, task)
        return TaskDto.model_validate(task)

    async def add_for_user(self, db: AsyncSession, user_id: int, task_data: TaskBase) -> TaskDto:
        task = Task(**task_data.model_dump(), user_id=user_id)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return TaskDto.model_validate(task)

    async def update(self, db: AsyncSession, task_id: int, patch_data: TaskOptional) -> TaskDto:
        task = await super().get_by_id(db, task_id)
        if not task:
            raise ValueError(f"Задача с ID {task_id} не найдена")
        update_data = patch_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await db.commit()
        await db.refresh(task)
        return TaskDto.model_validate(task)

    async def delete(self, db: AsyncSession, task_dto: TaskDto) -> None:
        result = await db.execute(select(Task).where(Task.id == task_dto.id))
        task = result.scalar_one_or_none()
        if task:
            await super().delete(db, task)
