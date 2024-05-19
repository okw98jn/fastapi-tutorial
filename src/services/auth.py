from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlmodel import select

from src.models.user import User
from src.services.base import BaseService
from src.settings.app import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY
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

        user = self.session.exec(select(User).where(User.email == email)).first()

        if not user:
            return None

        if not HashUtil.verify_password(password, user.password):
            return None

        return user

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
