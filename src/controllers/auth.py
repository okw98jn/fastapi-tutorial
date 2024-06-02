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

        if not user or not user.id:
            raise LoginFailedException()

        return auth_service.create_jwt_token(user.id)

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

        Raises:
            LoginFailedException: 認証エラー
        """

        user = auth_service.create_user(form_data.username, form_data.password)

        if not user.id:
            raise LoginFailedException()

        return auth_service.create_jwt_token(user.id)

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

    @classmethod
    async def google_auth_callback(
        cls,
        code: str,
        auth_service: AuthService = Depends(AuthService),
    ) -> Token:
        """
        Google認証コールバックAPI

        Returns:
            Token: トークン
        """
        google_access_token = await auth_service.get_google_access_token(code)
        user_email = await auth_service.get_google_user_email(google_access_token)

        return auth_service.create_jwt_token(1)
