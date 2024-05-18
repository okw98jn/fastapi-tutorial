from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    pass


async def not_found_exception_handler(
    request: Request, exc: NotFoundException
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Not Found"})
