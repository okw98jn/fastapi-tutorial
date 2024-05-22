from typing import Sequence

from sqlmodel import select

from src.exceptions.conflict_exception import ConflictException
from src.exceptions.not_found_exception import NotFoundException
from src.models.user import User, UserCreate, UserUpdate
from src.services.base import BaseService
from src.settings.logger import logger
from src.utils.hash import HashUtil


class UserService(BaseService):
    def get_users(self, offset: int, limit: int) -> Sequence[User]:
        """
        ユーザー一覧を返すメソッド

        Args:
            offset (int): 取得開始位置
            limit (int): 取得件数

        Returns:
            Sequence[User]: ユーザー一覧
        """

        return self.session.exec(select(User).offset(offset).limit(limit)).all()

    def get_user(self, user_id: int) -> User:
        """
        ユーザーIDに対応するユーザー情報を返すメソッド

        Args:
            user_id (int): ユーザーID

        Returns:
            User: ユーザー情報

        Raises:
            NotFoundException: ユーザーが見つからない場合の例外
        """

        user = self.session.get(User, user_id)

        if not user:
            logger.error(f"User not found. user_id: {user_id}")
            raise NotFoundException()

        return user

    def create_user(self, create_data: UserCreate) -> User:
        """
        ユーザー情報を登録するメソッド

        Args:
            create_data (UserCreate): ユーザー情報

        Returns:
            User: 登録したユーザー情報

        Raises:
            CustomValidationException: メールアドレスが重複している場合の例外
            Exception: 登録に失敗した場合の例外
        """

        try:
            if self.get_user_id_by_email(create_data.email):
                raise ConflictException(message="Email already exists")

            user = User.model_validate(create_data)
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

    def update_user(self, user: User, update_data: UserUpdate) -> User:
        """
        ユーザー情報を更新するメソッド

        Args:
            user (User): ユーザー
            update_data (UserUpdate): 更新するユーザー情報

        Returns:
            User: 更新したユーザー情報

        Raises:
            CustomValidationException: メールアドレスが重複している場合の例外
            Exception: 更新に失敗した場合の例外
        """

        try:
            registered_user_id = self.get_user_id_by_email(update_data.email or "")
            if registered_user_id and registered_user_id != user.id:
                raise ConflictException(message="Email already exists")

            user.sqlmodel_update(update_data.model_dump(exclude_unset=True))

            self.session.commit()
            self.session.refresh(user)

            return user
        except ConflictException:
            # メールアドレス重複エラーはログ出力しない
            raise
        except Exception as e:
            logger.error(e)
            raise e

    def delete_user(self, user: User) -> None:
        """
        ユーザーIDに対応するユーザー情報を削除するメソッド

        Args:
            user (User): 削除するユーザー

        Raises:
            Exception: 削除に失敗した場合の例外
        """

        try:
            self.session.delete(user)
            self.session.commit()
        except Exception as e:
            logger.error(e)
            raise e

    def get_user_id_by_email(self, email: str) -> int | None:
        """
        メールアドレスに対応するユーザーidを返すメソッド

        Args:
            email (str): メールアドレス

        Returns:
            int | None: ユーザーID| ユーザーが存在しない場合はNone
        """

        return self.session.exec(select(User.id).where(User.email == email)).first()
