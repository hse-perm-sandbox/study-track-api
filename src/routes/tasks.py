from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.repositories.task import TaskRepository
from src.schemas.task import TaskBase, TaskDto, TaskOptional
from src.db.models.user import User
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

task_repo = TaskRepository()


@router.get(
    "/",
    summary="Получить список задач пользователя",
    description="Возвращает все задачи, привязанные к указанному пользователю",
    response_model=list[TaskDto],
)
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await task_repo.get_all(db)


@router.post(
    "/",
    summary="Создать новую задачу",
    description="Добавляет новую задачу для указанного пользователя",
    response_model=TaskDto,
    status_code=201,
)
async def post_task(
    task_data: TaskBase = Body(...),
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_repo.add_for_user(db, current_user.id, task_data)


@router.patch(
    "/{id}",
    summary="Обновить задачу",
    description="Изменяет данные задачи по ID",
    response_model=TaskDto,
)
async def patch_task(
    task_id: int,
    task_data: TaskOptional = Body(...),
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await task_repo.get_by_id(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Задача не найдена или доступ запрещён")
    return await task_repo.update(db, task_id, task_data)


@router.delete(
    "/{id}",
    summary="Удалить задачу",
    description="Удаляет задачу по ID",
    status_code=204,
)

async def delete_task(
    id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await task_repo.get_by_id(db, id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    await task_repo.delete(db, task)
    return Response(status_code=204)
