from fastapi import FastAPI

from src.exceptions.exception_handlers import add_exception_handlers
from src.middlewares.log import LogMiddleware
from src.routes import auth, user

app = FastAPI()

app.add_middleware(LogMiddleware)

# エラーハンドラーを一括で登録する
add_exception_handlers(app)

# ルーターを登録する
routers = [
    user.router,
    auth.router,
]

APP_PREFIX = "/api"

for router in routers:
    app.include_router(router, prefix=APP_PREFIX)
