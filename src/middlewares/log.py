import time

from fastapi import Request, Response

from src.logger import logger


async def log_middleware(request: Request, call_next) -> Response:
    """
    ログミドルウェア
    """

    start_time = time.time()
    client_ip = request.client.host if request.client else "Unknown"

    # リクエストのログを記録
    request_body = await request.body()
    request_log_dict = {
        "client_ip": client_ip,
        "url": str(request.url),
        "method": request.method,
        "query_params": str(request.query_params),
        "headers": dict(request.headers),
        "body": request_body.decode("utf-8"),
    }
    logger.info(f"Request: {request_log_dict}")

    # レスポンスのログを記録するための準備
    response = await call_next(request)
    response_body = b""

    async for chunk in response.body_iterator:
        response_body += chunk

    response_log_dict = {
        "client_ip": client_ip,
        "url": str(request.url),
        "method": request.method,
        "status_code": response.status_code,
        "body": response_body.decode("utf-8"),
        "processing_time": f"{time.time() - start_time:.4f} seconds",
    }
    logger.info(f"Response: {response_log_dict}")

    # 新しいレスポンスオブジェクトを作成して返す
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
