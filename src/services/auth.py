import urllib.parse
from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlmodel import select

from src.exceptions.conflict_exception import ConflictException
from src.models.user import User
from src.services.base import BaseService
from src.settings.app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    GOOGLE_AUTHORIZATION_URL,
    GOOGLE_CALLBACK_URL,
    GOOGLE_CLIENT_ID,
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
