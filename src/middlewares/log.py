import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.settings.logger import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        ログミドルウェア

        Args:
            request (Request): リクエストオブジェクト
            call_next: 次のミドルウェアまたはエンドポイントハンドラーを呼び出す関数

        Returns:
            Response: レスポンスオブジェクト
        """

        start_time = time.time()
        client_ip = request.client.host if request.client else "Unknown"

        # リクエストのログを記録
        await self.log_request(request, client_ip)

        try:
            # レスポンスの処理
            response = await call_next(request)
            response_body = await self.get_response_body(response)

            # レスポンスのログを記録
            await self.log_response(
                request, response, response_body, client_ip, start_time
            )

            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        except Exception as e:
            # 例外発生時のレスポンスログを記録
            await self.log_error_response(request, client_ip, start_time)

            # 例外発生時のレスポンスはエラーハンドラーに任せる
            raise e

    async def log_request(self, request: Request, client_ip: str) -> None:
        """
        リクエストのログを記録

        Args:
            request (Request): リクエストオブジェクト
            client_ip (str): クライアントIPアドレス

        Returns:
            None
        """

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

    async def log_response(
        self,
        request: Request,
        response: Response,
        response_body: bytes,
        client_ip: str,
        start_time: float,
    ) -> None:
        """
        レスポンスのログを記録

        Args:
            request (Request): リクエストオブジェクト
            response (Response): レスポンスオブジェクト
            response_body (bytes): レスポンスボディ
            client_ip (str): クライアントIPアドレス
            start_time (float): リクエスト処理開始時刻

        Returns:
            None
        """

        response_log_dict = {
            "client_ip": client_ip,
            "url": str(request.url),
            "method": request.method,
            "status_code": response.status_code,
            "body": response_body.decode("utf-8"),
            "processing_time": f"{time.time() - start_time:.4f} seconds",
        }
        logger.info(f"Response: {response_log_dict}")

    async def log_error_response(
        self, request: Request, client_ip: str, start_time: float
    ) -> None:
        """
        エラーレスポンスのログを記録

        Args:
            request (Request): リクエストオブジェクト
            client_ip (str): クライアントIPアドレス
            start_time (float): リクエスト処理開始時刻

        Returns:
            None
        """

        error_response_log_dict = {
            "client_ip": client_ip,
            "url": str(request.url),
            "method": request.method,
            "status_code": 500,
            "body": {"detail": "Internal Server Error"},
            "processing_time": f"{time.time() - start_time:.4f} seconds",
        }
        logger.info(f"Response: {error_response_log_dict}")

    async def get_response_body(self, response: Response) -> bytes:
        """
        レスポンスボディを取得

        Args:
            response (Response): レスポンスオブジェクト

        Returns:
            bytes: レスポンスボディ
        """

        response_body = b""
        async for chunk in response.body_iterator:  # type: ignore
            response_body += chunk

        return response_body
