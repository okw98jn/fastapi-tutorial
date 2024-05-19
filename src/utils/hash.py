from passlib.context import CryptContext


class HashUtil:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, plain_password: str) -> str:
        """
        パスワードのハッシュ化を行うメソッド

        Args:
            plain_password (str): 平文パスワード

        Returns:
            str: ハッシュ化されたパスワード
        """

        return cls.pwd_context.hash(plain_password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        パスワードの検証を行うメソッド

        Args:
            plain_password (str): 平文パスワード
            hashed_password (str): ハッシュ化されたパスワード

        Returns:
            bool: パスワードが一致するかどうか
        """

        return cls.pwd_context.verify(plain_password, hashed_password)
