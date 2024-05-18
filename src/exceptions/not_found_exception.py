from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)


async def not_found_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, NotFoundException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
