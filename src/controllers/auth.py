from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

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
        ログイン処理を行うメソッド

        Args:
            form_data (OAuth2PasswordRequestForm): フォームデータ
            auth_service (AuthService): AuthServiceのインスタンス

        Returns:
            Token: トークン
        """

        user = auth_service.authenticate_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return Token(
            access_token=auth_service.create_access_token(data={"sub": user.email}),
            token_type="bearer",
        )
