import urllib.parse
from datetime import datetime, timedelta, timezone

import httpx
from jose import jwt
from sqlmodel import select

from src.exceptions.conflict_exception import ConflictException
from src.exceptions.login_failed_exception import LoginFailedException
from src.models.user import Token, User
from src.services.base import BaseService
from src.settings.app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    GOOGLE_AUTHORIZATION_URL,
    GOOGLE_CALLBACK_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_TOKEN_URL,
    GOOGLE_USER_INFO_URL,
    JWT_SECRET_KEY,
)
from src.settings.logger import logger
from src.utils.hash import HashUtil


class AuthService(BaseService):
    def authenticate_user(self, email: str, password: str) -> User | None:
        """
        ユーザー認証を行うメソッド

        Args:
            email (str): メールアドレス
            password (str): パスワード

        Returns:
            User|None: ユーザー情報またはNone
        """

        user = self.get_user_id_by_email(email)

        if not user:
            return None

        if not HashUtil.verify_password(password, user.password):
            return None

        return user

    def create_user(self, email: str, password: str) -> User:
        """
        ユーザーを作成するメソッド

        Args:
            email (str): メールアドレス
            password (str): パスワード

        Returns:
            User: ユーザー

        Raises:
            ConflictException: メールアドレスが重複している場合
        """

        try:
            if self.get_user_id_by_email(email):
                raise ConflictException(message="Email already exists")

            user = User.model_validate({"email": email, "password": password})
            user.password = HashUtil.get_password_hash(user.password)

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            return user
        except ConflictException:
            # メールアドレス重複エラーはログ出力しない
            raise
        except Exception as e:
            logger.error(e)
            raise e

    def create_access_token(self, data: dict) -> str:
        """
        アクセストークンを生成するメソッド

        Args:
            data (dict): データ

        Returns:
            str: アクセストークン
        """

        to_encode = data.copy()

        jst = timezone(timedelta(hours=9))

        expire = datetime.now(jst) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    def create_jwt_token(self, user_id: int) -> Token:
        """
        JWTトークンを生成するメソッド

        Args:
            user_id (int): ユーザーID

        Returns:
            Token: JWTトークン
        """

        return Token(
            # JWTトークンのdecodeでエラーが発生するためstrに変換
            access_token=self.create_access_token(data={"sub": str(user_id)}),
            token_type="bearer",
        )

    def get_user_id_by_email(self, email: str) -> User | None:
        """
        メールアドレスに対応するユーザーを返すメソッド

        Args:
            email (str): メールアドレス

        Returns:
            User | None: ユーザー| ユーザーが存在しない場合はNone
        """

        return self.session.exec(select(User).where(User.email == email)).first()

    def get_google_auth_url(self) -> str:
        """
        Google認証URLを取得するメソッド

        Returns:
            str: Google認証URL
        """

        params = {
            "response_type": "code",
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_CALLBACK_URL,
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        return f"{GOOGLE_AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"

    async def get_google_access_token(self, code: str) -> str:
        """
        Googleの認証コードを使用してアクセストークンを取得する

        Args:
            code (str): Google認証コード

        Returns:
            str: Googleアクセストークン

        Raises:
            LoginFailedException: 認証エラー
        """

        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": GOOGLE_CALLBACK_URL,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                },
            )

        token_response_json = token_response.json()

        if token_response.is_error:
            logger.error(token_response_json)
            raise LoginFailedException()

        return token_response_json.get("access_token")

    async def get_google_user_email(self, access_token: str) -> str:
        """
        Googleアクセストークンを使用してユーザーのメールアドレスを取得する

        Args:
            access_token (str): Googleアクセストークン

        Returns:
            str: ユーザーのメールアドレス

        Raises:
            LoginFailedException: 認証エラー
        """

        async with httpx.AsyncClient() as client:
            user_info_response = await client.get(
                GOOGLE_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )

        user_info_response_json = user_info_response.json()

        if user_info_response.is_error:
            logger.error(user_info_response_json)
            raise LoginFailedException()

        return user_info_response_json.get("email")
