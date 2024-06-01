from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

from src.settings.app import ALGORITHM, JWT_SECRET_KEY


class AuthenticateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        リクエストにトークンが含まれているかを確認し
        トークンが正しいかを確認するミドルウェア

        Args:
            request (Request): リクエスト
            call_next (Callable): 次のミドルウェア

        Returns:
            JSONResponse: レスポンス
        """

        # Swagger UIのリクエストは認証をスキップ
        if request.url.path.startswith("/api") is False:
            return await call_next(request)

        # ログインAPIは認証をスキップ
        if (
            request.url.path == "/api/auth/login"
            or request.url.path == "/api/auth/register"
        ):
            return await call_next(request)

        token = request.headers.get("Authorization")

        if token is None:
            # TODO: カスタム例外ハンドラーを使用するとエラーになるため一旦ここだけ直接レスポンスを返す(raiseするとエラーになる)
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        try:
            # "Bearer <token>"からトークン部分を抽出
            token = token.split(" ")[1]

            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")

            if user_id is None:
                return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

            request.state.user_id = user_id

            return await call_next(request)
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
