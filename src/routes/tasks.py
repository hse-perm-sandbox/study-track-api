from fastapi import APIRouter, Body, HTTPException, Path, Response
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/api/tasks",
)

last_task_id = 2
tasks = [
    {
        "id": 1,
        "title": "Сделать домашнее задание",
        "description": "Упражнения по алгебре",
        "priority": "high",
        "deadline": "2025-05-20"
    },
    {
        "id": 2,
        "title": "Подготовить доклад",
        "description": "История. Тема: Вторая мировая война",
        "priority": "medium",
        "deadline": "2025-05-25"
    }
]

#получить все задачи
@router.get(
    "/",
    summary="Получить список всех задач",
    description="Возвращает все задачи системе",
)
async def get_tasks():
    return tasks

#получить задачу по id
@router.get(
    "/{id}",
    summary="Получить пользователя по ID",
    description="Ищет пользователя по указанному ID",
)
async def get_task(id: int = Path(...)):
    task = next((x for x in tasks if x["id"] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

#удалить задачу
@router.delete(
    "/{id}",
    summary="Удалить задачу",
    description="Удаляет задачу по указанному ID",
)
async def delete_task(response: Response, id: int = Path()):
    global tasks
    task = next((x for x in tasks if x["id"] == id))
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

#создать задачу
@router.post(
    "/",
    summary="Создать новую задачу",
    description="Добавляет новую задачу в список",
)
async def post_task(task_data=Body()):
    global last_task_id
    last_task_id += 1
    task_data["id"] = last_task_id

    task_data.setdefault("priority", "medium")
    task_data.setdefault("description", "")
    task_data.setdefault("deadline", "")

    tasks.append(task_data)
    return JSONResponse(content=task_data, status_code=201)

#обновление задачи 
@router.patch(
    "/{id}",
    summary="Обновить данные о задаче",
    description="Изменяет имя или возраст пользователя по ID",
)
async def patch_task(id: int = Path(), task_data=Body()):
    task = next((x for x in tasks if x["id"] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task["title"] = task_data.get("title", task["title"])
    task["description"] = task_data.get("description", task["description"])
    task["priority"] = task_data.get("priority", task["priority"])
    task["deadline"] = task_data.get("deadline", task["deadline"])

    return task
