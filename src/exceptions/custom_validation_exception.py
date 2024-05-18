from fastapi import Request
from fastapi.responses import JSONResponse


class CustomValidationException(Exception):
    def __init__(self, loc: str, msg: str):
        self.loc = loc
        self.msg = msg


async def custom_validation_exception_handler(
    request: Request, exc: CustomValidationException
) -> JSONResponse:
    return JSONResponse(
        status_code=422, content={"detail": {"loc": exc.loc, "msg": exc.msg}}
    )
