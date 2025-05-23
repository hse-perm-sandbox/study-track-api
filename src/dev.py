import uvicorn

from src.main import create_app

app = create_app()


def start():
    """Запускает приложение в dev-режиме."""
    uvicorn.run("src.dev:app", host="0.0.0.0", port=8080, reload=True)

from src.routes.auth import router as auth_router
app.include_router(auth_router)

if __name__ == "__main__":
    start()
