from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.exceptions.authentication_exception import AuthenticationException
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
            AuthenticationException: 認証エラー
        """

        user = auth_service.authenticate_user(form_data.username, form_data.password)

        if not user:
            raise AuthenticationException()

        return Token(
            access_token=auth_service.create_access_token(data={"sub": user.id}),
            token_type="bearer",
        )
