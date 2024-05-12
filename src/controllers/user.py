from fastapi import Depends, Query

from src.models.user import UserCreate, UserPublic, UserUpdate
from src.repositories.user import UserRepository


class UserController:
    @classmethod
    async def index(
        cls,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        user_repository: UserRepository = Depends(UserRepository),
    ) -> list[UserPublic]:
        """
        ユーザー一覧API

        Args:
            offset (int): 取得開始位置
            limit (int): 取得件数

        Returns:
            list[UserPublic]: ユーザー一覧
        """

        return [
            UserPublic.model_validate(user)
            for user in user_repository.get_users(offset, limit)
        ]

    @classmethod
    async def show(
        cls, user_id: int, user_repository: UserRepository = Depends(UserRepository)
    ) -> UserPublic:
        """
        ユーザー詳細API

        Args:
            user_id (int): ユーザーID
            user_repository (UserRepository): ユーザーリポジトリ

        Returns:
            UserPublic: ユーザー情報
        """

        return UserPublic.model_validate(user_repository.get_user(user_id))

    @classmethod
    async def create(
        cls, user: UserCreate, user_repository: UserRepository = Depends(UserRepository)
    ) -> UserPublic:
        """
        ユーザー登録API

        Args:
            user (UserCreate): ユーザー情報

        Returns:
            UserPublic: 登録したユーザー情報
        """

        return UserPublic.model_validate(user_repository.create_user(user))

    @classmethod
    async def update(
        cls,
        user_id: int,
        user: UserUpdate,
        user_repository: UserRepository = Depends(UserRepository),
    ) -> UserPublic:
        """
        ユーザー更新API

        Args:
            user_id (int): ユーザーID
            user (UserUpdate): ユーザー情報
            user_repository (UserRepository): ユーザーリポジトリ

        Returns:
            UserPublic: 更新したユーザー情報
        """

        return UserPublic.model_validate(user_repository.update_user(user_id, user))

    @classmethod
    async def delete(
        cls, user_id: int, user_repository: UserRepository = Depends(UserRepository)
    ) -> dict[str, bool]:
        """
        ユーザー情報を削除するクラスメソッド

        Args:
            user_id (int): ユーザーID
            user_repository (UserRepository): ユーザーリポジトリ

        Returns:
            dict[str, str]: 削除完了メッセージ
        """

        user_repository.delete_user(user_id)

        return {"ok": True}
