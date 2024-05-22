from fastapi import FastAPI

from src.exceptions.exception_handlers import APIExceptionHandler
from src.middlewares.authenticate import AuthenticateMiddleware
from src.middlewares.log import LogMiddleware
from src.routes import auth, user

app = FastAPI(exception_handlers=APIExceptionHandler.handlers())

app.add_middleware(LogMiddleware)
app.add_middleware(AuthenticateMiddleware)

# ルーターを登録する
routers = [
    user.router,
    auth.router,
]

APP_PREFIX = "/api"

for router in routers:
    app.include_router(router, prefix=APP_PREFIX)
