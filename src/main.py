from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.middlewares.log import log_middleware
from src.routes import user

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(user.router)
