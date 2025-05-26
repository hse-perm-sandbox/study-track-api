from fastapi import APIRouter, Body, HTTPException, Path, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.repositories.task import TaskRepository
from src.schemas.task import TaskDto, TaskOptional, TaskBase

router = APIRouter(
    prefix="/api/users/{user_id}/tasks",
)

task_repo = TaskRepository()


@router.get(
    "/",
    summary="Получить список задач пользователя",
    description="Возвращает все задачи, привязанные к указанному пользователю",
    response_model=list[TaskDto],
)
async def get_tasks(user_id: int = Path(), db: AsyncSession = Depends(get_db)):
    return await task_repo.get_all_by_user(db, user_id)


@router.post(
    "/",
    summary="Создать новую задачу",
    description="Добавляет новую задачу для указанного пользователя",
    response_model=TaskDto,
    status_code=201,
)
async def post_task(
    user_id: int = Path(),
    task_data: TaskBase = Body(...),
    db: AsyncSession = Depends(get_db),
):
    return await task_repo.add_for_user(db, user_id, task_data)


@router.patch(
    "/{id}",
    summary="Обновить задачу",
    description="Изменяет данные задачи по ID",
    response_model=TaskDto,
)
async def patch_task(
    user_id: int = Path(),
    id: int = Path(),
    task_data: TaskOptional = Body(...),
    db: AsyncSession = Depends(get_db),
):
    task = await task_repo.update(db, id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.delete(
    "/{id}",
    summary="Удалить задачу",
    description="Удаляет задачу по ID",
    status_code=204,
)
async def delete_task(
    user_id: int = Path(),
    id: int = Path(),
    db: AsyncSession = Depends(get_db),
):
    task = await task_repo.get_by_id(db, id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    await task_repo.delete(db, task)
    return Response(status_code=204)
