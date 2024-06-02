from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions.login_failed_exception import LoginFailedException
from src.models.user import Token
from src.services.auth import AuthService


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

    @classmethod
    async def register(
        cls,
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(AuthService),
    ) -> Token:
        """
        サインアップAPI

        Args:
            form_data (OAuth2PasswordRequestForm): フォームデータ
            auth_service (AuthService): AuthServiceのインスタンス

        Returns:
            Token: トークン
        """

        user = auth_service.create_user(form_data.username, form_data.password)

        return Token(
            # JWTトークンのdecodeでエラーが発生するためstrに変換
            access_token=auth_service.create_access_token(data={"sub": str(user.id)}),
            token_type="bearer",
        )

    @classmethod
    async def google_auth_url(
        cls,
        auth_service: AuthService = Depends(AuthService),
    ) -> str:
        """
        Google認証URL取得API

        Returns:
            str: Google認証URL
        """

        return auth_service.get_google_auth_url()
