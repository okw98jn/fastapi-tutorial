from typing import Sequence

from sqlmodel import select

from src.exceptions.not_found_exception import NotFoundException
from src.models.user import User, UserCreate, UserUpdate
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def get_users(self, offset: int, limit: int) -> Sequence[User]:
        """
        ユーザー一覧を返すメソッド

        Args:
            offset (int): 取得開始位置
            limit (int): 取得件数

        Returns:
            list[User]: ユーザー一覧
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
            raise NotFoundException()

        return user

    def create_user(self, create_data: UserCreate) -> User:
        """
        ユーザー情報を登録するメソッド

        Args:
            create_data (UserCreate): ユーザー情報

        Returns:
            User: 登録したユーザー情報
        """

        user = User.model_validate(create_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def update_user(self, user_id: int, update_data: UserUpdate) -> User:
        """
        ユーザー情報を更新するメソッド

        Args:
            user_id (int): ユーザーID
            update_data (UserUpdate): 更新するユーザー情報

        Returns:
            User: 更新したユーザー情報
        """

        update_user_data = update_data.model_dump(exclude_unset=True)

        user = self.get_user(user_id)
        user.sqlmodel_update(update_user_data)

        self.session.commit()
        self.session.refresh(user)

        return user

    def delete_user(self, user_id: int) -> None:
        """
        ユーザーIDに対応するユーザー情報を削除するメソッド

        Args:
            user_id (int): ユーザーID
        """

        user = self.get_user(user_id)
        self.session.delete(user)
        self.session.commit()
