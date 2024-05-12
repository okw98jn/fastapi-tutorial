from fastapi import Request, Response

from src.logger import logger


async def log_middleware(request: Request, call_next) -> Response:
    """
    ログミドルウェア
    """

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "query_params": request.query_params,
        "headers": request.headers,
        "body": await request.body(),
    }

    logger.info(log_dict)

    response = await call_next(request)

    return response
