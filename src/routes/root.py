from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
)


@router.get(
    "/",
    summary="Тестовый endpoint",
    description="Тестовый endpoint для демонстрации работы API",
    response_description="Возвращает объект с двумя полями: value и description",
)
async def get_root():
    return {"value": "Some test value", "description": "Test value description"}
