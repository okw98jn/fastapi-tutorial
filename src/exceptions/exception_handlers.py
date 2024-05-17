from fastapi import FastAPI

from src.exceptions.generic_exception import generic_exception_handler
from src.exceptions.not_found_exception import (
    NotFoundException,
    not_found_exception_handler,
)


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
