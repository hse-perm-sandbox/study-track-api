from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.models.category import Category
from src.db.repositories.category import CategoryRepository
from src.schemas.category import CategoryBase, CategoryDto, CategoryOptional

router = APIRouter(prefix="/api/categories", tags=["Categories"])

category_repo = CategoryRepository()


@router.get(
    "/",
    summary="Получить список категорий",
    description="Возвращает все категории в системе",
    response_model=list[CategoryDto],
)
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await category_repo.get_all(db)


@router.get(
    "/{id}",
    summary="Получить категорию по ID",
    description="Ищет категорию по указанному ID",
    response_model=CategoryDto,
)
async def get_category(id: int = Path(), db: AsyncSession = Depends(get_db)):
    category = await category_repo.get_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.delete(
    "/{id}",
    summary="Удалить категорию",
    description="Удаляет категорию по указанному ID",
    status_code=204,
)
async def delete_category(id: int = Path(), db: AsyncSession = Depends(get_db)):
    category = await category_repo.get_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    await category_repo.delete(db, category)
    return Response(status_code=204)


@router.post(
    "/",
    summary="Создать новую категорию",
    description="Добавляет новую категорию в базу данных",
    response_model=CategoryDto,
    status_code=201,
)
async def post_category(
    category_data: CategoryBase = Body(...), db: AsyncSession = Depends(get_db)
):
    category = Category(**category_data.dict())
    return await category_repo.add(db, category)


@router.patch(
    "/{id}",
    summary="Обновить категорию",
    description="Изменяет название категории по ID",
    response_model=CategoryDto,
)
async def patch_category(
    id: int = Path(),
    category_data: CategoryOptional = Body(...),
    db: AsyncSession = Depends(get_db),
):
    category = await category_repo.update(db, id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category
