from fastapi import HTTPException, Request
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

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
            Response: レスポンス

        Raises:
            HTTPException: トークンが不正な場合
        """

        # Swagger UIのリクエストは認証をスキップ
        if request.url.path.startswith("/api") is False:
            return await call_next(request)

        # ログインAPIは認証をスキップ
        if request.url.path == "/api/auth/login":
            return await call_next(request)

        token = request.headers.get("Authorization")

        if token is None:
            return JSONResponse(status_code=401, content={"detail": "Missing token"})

        try:
            # "Bearer <token>"からトークン部分を抽出
            token = token.split(" ")[1]

            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")

            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")

            request.state.user = username

            return await call_next(request)
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
