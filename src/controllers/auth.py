from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.exceptions.login_failed_exception import LoginFailedException
from src.services.auth import AuthService


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AuthController:
    @classmethod
    async def login(
        cls,
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(AuthService),
    ) -> Token:
        """
        ログインAPI

        Args:
            form_data (OAuth2PasswordRequestForm): フォームデータ
            auth_service (AuthService): AuthServiceのインスタンス

        Returns:
            Token: トークン

        Raises:
            LoginFailedException: 認証エラー
        """

        user = auth_service.authenticate_user(form_data.username, form_data.password)

        if not user:
            raise LoginFailedException()

        return Token(
            # JWTトークンのdecodeでエラーが発生するためstrに変換
            access_token=auth_service.create_access_token(data={"sub": str(user.id)}),
            token_type="bearer",
        )
