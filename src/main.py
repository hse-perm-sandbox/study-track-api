from fastapi import FastAPI
import uvicorn


from src.routes.users import router as test_root_router


def start():
    app = FastAPI(
        title="ADD APP TITLE...",
        description="API для ...",
    )
    app.include_router(router=test_root_router)

    uvicorn.run(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    start()
