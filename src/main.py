from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from src.routes.users import router as user_router


def create_app() -> FastAPI:
    """Создает экземпляр приложения."""
    app = FastAPI(
        title="Study Track",
        description="Study Track — web-приложение, ориентированное на студентов, с функциями, специально адаптированными под учебный процесс: задачи, категории, приоритеты, напоминания, календарное отображение.",
    )
    app.include_router(router=user_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def start():
    """Запускает приложение."""
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    start()
