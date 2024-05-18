from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.exceptions.custom_validation_exception import (
    CustomValidationException,
    custom_validation_exception_handler,
)
from src.exceptions.generic_exception import generic_exception_handler
from src.exceptions.not_found_exception import (
    NotFoundException,
    not_found_exception_handler,
)
from src.exceptions.validation_exception import validation_exception_handler


def add_exception_handlers(app: FastAPI):
    # 404
    app.add_exception_handler(
        NotFoundException, not_found_exception_handler  # type: ignore
    )

    # 422(標準バリデーション)
    app.add_exception_handler(
        RequestValidationError, validation_exception_handler  # type: ignore
    )

    # 422(カスタムバリデーション)
    app.add_exception_handler(
        CustomValidationException, custom_validation_exception_handler  # type: ignore
    )

    # 500
    app.add_exception_handler(Exception, generic_exception_handler)  # type: ignore
