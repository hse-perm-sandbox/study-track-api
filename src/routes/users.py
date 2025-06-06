from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.models.user import User
from src.db.repositories.category import CategoryRepository
from src.db.repositories.task import TaskRepository
from src.db.repositories.user import UserRepository
from src.schemas.category import CategoryDto
from src.schemas.task import TaskDto
from src.schemas.user import UserBase, UserDto, UserOptional
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/users", tags=["Users"])

user_repo = UserRepository()
task_repo = TaskRepository()
category_repo = CategoryRepository()


@router.get(
    "/",
    summary="Получить список пользователей",
    description="Возвращает всех пользователей в системе",
    response_model=list[UserDto],
)
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_repo.get_all(db)


@router.get(
    "/{id}",
    summary="Получить пользователя по ID",
    description="Ищет пользователя по указанному ID",
    response_model=UserDto,
)
async def get_user(id: int = Path(), db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.get(
    "/{id}/tasks",
    summary="Получить список задач пользователя",
    description="Возвращает все задачи, привязанные к указанному пользователю",
    response_model=list[TaskDto],
)
async def get_tasks_by_user(id: int = Path(), db: AsyncSession = Depends(get_db)):
    return await task_repo.get_all_by_user(db, id)


@router.get(
    "/{id}/categories",
    summary="Получить список категорий пользователя",
    description="Возвращает все категории, привязанные к указанному пользователю",
    response_model=list[CategoryDto],
)
async def get_categories_by_user(id: int = Path(), db: AsyncSession = Depends(get_db)):
    return await category_repo.get_all_by_user(db, id)


@router.delete(
    "/{id}",
    summary="Удалить пользователя",
    description="Удаляет пользователя по указанному ID",
    status_code=204,
)
async def delete_user(id: int = Path(), db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await user_repo.delete(db, user)
    return Response(status_code=204)


@router.post(
    "/",
    summary="Создать нового пользователя",
    description="Добавляет нового пользователя в базу данных",
    response_model=UserDto,
    status_code=201,
)
async def post_user(user_data: UserBase = Body(...), db: AsyncSession = Depends(get_db)):
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=AuthService.get_password_hash(user_data.password),
    )
    return await user_repo.add(db, user)


@router.patch(
    "/{id}",
    summary="Обновить данные пользователя",
    description="Изменяет имя или возраст пользователя по ID",
    response_model=UserDto,
)
async def patch_user(
    id: int = Path(),
    user_data: UserOptional = Body(...),
    db: AsyncSession = Depends(get_db),
):
    user = await user_repo.update(db, id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
