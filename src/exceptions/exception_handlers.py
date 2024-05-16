from fastapi import FastAPI

from src.exceptions.not_found_exception import (
    NotFoundException,
    not_found_exception_handler,
)


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
