from fastapi import APIRouter, Body, HTTPException, Path, Response
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/api/users",
)

last_id = 2
users = [{"name": "Timur", "age": 18, "id": 1}, {"name": "Kox", "age": 23, "id": 2}]


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
async def get_user(id: int = Path()):
    filtered_users = [x for x in users if x["id"] == id]
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users[0]


@router.delete(
    "/{id}",
    summary="Удалить пользователя",
    description="Удаляет пользователя по указанному ID",
)
async def delete_user(response: Response, id: int = Path()):
    global users
    filtered_users = [x for x in users if x["id"] == id]
    if not filtered_users:
        raise HTTPException(status_code=404)
    users = [x for x in users if x["id"] != id]
    response.status_code = 204


@router.post(
    "/",
    summary="Создать нового пользователя",
    description="Добавляет нового пользователя в список",
)
async def post_user(user_data=Body()):
    global last_id
    last_id += 1
    user_data["id"] = last_id
    users.append(user_data)
    return JSONResponse(content=user_data, status_code=201)


@router.patch(
    "/{id}",
    summary="Обновить данные пользователя",
    description="Изменяет имя или возраст пользователя по ID",
)
async def patch_user(id=Path(), user_data=Body()):
    filtered_users = [x for x in users if x["id"] == id]
    if not filtered_users:
        raise HTTPException(status_code=404)
    if "name" in user_data:
        filtered_users[0]["name"] = user_data["name"]
    if "age" in user_data:
        filtered_users[0]["age"] = user_data["age"]
    return filtered_users[0]
