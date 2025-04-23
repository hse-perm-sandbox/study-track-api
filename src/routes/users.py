from fastapi import APIRouter, Body, Path


router = APIRouter(
    prefix="/api/users",
)

users = [{"name": "Timur", "age": 18, "id": 1}, {"name": "Kox", "age": 23, "id": 2}]

@router.get(
    "/",
    summary="Тестовый endpoint",
    description="Тестовый endpoint для демонстрации работы API",
    response_description="Возвращает объект с двумя полями: value и description",
)
async def get_users():
    return users

@router.get(
    "/{id}",
    summary="Тестовый endpoint",
    description="Тестовый endpoint для демонстрации работы API",
    response_description="Возвращает объект с двумя полями: value и description",
)
async def get_user(id: int =Path()):
    return [x for x in users if x["id"] == id]

@router.delete(
    "/{id}",
    summary="Тестовый endpoint",
    description="Тестовый endpoint для демонстрации работы API",
    response_description="Возвращает объект с двумя полями: value и description",
)
async def delete_user(id: int =Path()):
    cur = [x for x in users if x["id"] != id]
    users = cur

@router.post(
    "/",
    summary="Тестовый endpoint",
    description="Тестовый endpoint для демонстрации работы API",
    response_description="Возвращает объект с двумя полями: value и description",
)
async def post_user(user_data =Body()):
    users.append(user_data)
    return user_data

@router.patch(
    "/{id}",
    summary="Тестовый endpoint",
    description="Тестовый endpoint для демонстрации работы API",
    response_description="Возвращает объект с двумя полями: value и description",
)
async def patch_user(id = Path(), user_data =Body()):
    users.append(user_data)
    return user_data