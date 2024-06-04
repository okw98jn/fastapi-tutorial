from fastapi import Depends

from src.exceptions.login_failed_exception import LoginFailedException
from src.models.user import Token, UserCreate, UserPasswordLogin
from src.services.auth import AuthService


class AuthController:
    @classmethod
    async def login(
        cls,
        user_data: UserPasswordLogin,
        auth_service: AuthService = Depends(AuthService),
    ) -> Token:
        """
        ログインAPI

        Args:
            user_data (UserPasswordLogin): ユーザー情報
            auth_service (AuthService): AuthServiceのインスタンス

        Returns:
            Token: トークン

        Raises:
            LoginFailedException: 認証エラー
        """

        user = auth_service.authenticate_user(user_data)

        if not user or not user.id:
            raise LoginFailedException()

        return auth_service.create_jwt_token(user.id)

    @classmethod
    async def register(
        cls,
        user_data: UserCreate,
        auth_service: AuthService = Depends(AuthService),
    ) -> Token:
        """
        サインアップAPI

        Args:
            user_data (UserCreate): ユーザー情報
            auth_service (AuthService): AuthServiceのインスタンス

        Returns:
            Token: トークン

        Raises:
            LoginFailedException: 認証エラー
        """

        user = auth_service.create_user(user_data)

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
        user_data = await auth_service.get_google_user(google_access_token)

        return auth_service.create_jwt_token(1)
