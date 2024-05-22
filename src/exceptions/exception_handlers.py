from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exceptions.conflict_exception import ConflictException
from src.exceptions.not_found_exception import NotFoundException
from src.settings.logger import logger


class APIExceptionHandler:
    @classmethod
    def handlers(cls):
        return {
            NotFoundException: cls.not_found_exception_handler,
            ConflictException: cls.conflict_exception_handler,
            RequestValidationError: cls.validation_exception_handler,
            Exception: cls.generic_exception_handler,
        }

    @classmethod
    async def not_found_exception_handler(
        cls, request: Request, exc: NotFoundException
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    @classmethod
    async def conflict_exception_handler(
        cls, request: Request, exc: ConflictException
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @classmethod
    async def validation_exception_handler(
        cls, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # サーバー側でバリデーションエラーが発生したということはフロント側のバリデーション漏れか
        # 不正なリクエストが送られてきた可能性が高いためログにエラー内容を出力する
        logger.error(exc.errors())
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @classmethod
    async def generic_exception_handler(
        cls, request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )
