from fastapi import APIRouter, Body, Path


router = APIRouter(
    prefix="/api/users",
)

users = [
    {"name": "Timur", "age": 18, "id": 1}, 
    {"name": "Kox", "age": 23, "id": 2}
    ]

@router.get(
    "/",
    summary="Получить список пользователей",
    description="Возвращает всех пользователей в системе",
)
async def get_users():
    return users

@router.get(
    "/{id}",
    summary="Получить пользователя по ID",
    description="Ищет пользователя по указанному ID",
)
async def get_user(id: int =Path()):
    return [x for x in users if x["id"] == id]

@router.delete(
    "/{id}",
    summary="Удалить пользователя",
    description="Удаляет пользователя по указанному ID",
)
async def delete_user(id: int =Path()):
    global users 
    users = [x for x in users if x["id"] != id]

@router.post(
    "/",
    summary="Создать нового пользователя",
    description="Добавляет нового пользователя в список",
)
async def post_user(user_data =Body()):
    users.append(user_data)
    return user_data

@router.patch(
    "/{id}",
    summary="Обновить данные пользователя",
    description="Изменяет имя или возраст пользователя по ID",
)
async def patch_user(id = Path(), user_data =Body()):
    users.append(user_data)
    return user_data