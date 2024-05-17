from fastapi import Depends, Query

from src.models.user import UserCreate, UserPublic, UserUpdate
from src.services.user import UserService


class UserController:
    @classmethod
    async def index(
        cls,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        user_service: UserService = Depends(UserService),
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
            for user in user_service.get_users(offset, limit)
        ]

    @classmethod
    async def show(
        cls, user_id: int, user_service: UserService = Depends(UserService)
    ) -> UserPublic:
        """
        ユーザー詳細API

        Args:
            user_id (int): ユーザーID
            user_service (UserService): ユーザーサービス

        Returns:
            UserPublic: ユーザー情報
        """

        return UserPublic.model_validate(user_service.get_user(user_id))

    @classmethod
    async def create(
        cls, user: UserCreate, user_service: UserService = Depends(UserService)
    ) -> UserPublic:
        """
        ユーザー登録API

        Args:
            user (UserCreate): ユーザー情報

        Returns:
            UserPublic: 登録したユーザー情報
        """
        return UserPublic.model_validate(user_service.create_user(user))

    @classmethod
    async def update(
        cls,
        user_id: int,
        user: UserUpdate,
        user_service: UserService = Depends(UserService),
    ) -> UserPublic:
        """
        ユーザー更新API

        Args:
            user_id (int): ユーザーID
            user (UserUpdate): ユーザー情報
            user_service (UserService): ユーザーサービス

        Returns:
            UserPublic: 更新したユーザー情報
        """

        return UserPublic.model_validate(
            user_service.update_user(user_service.get_user(user_id), user)
        )

    @classmethod
    async def delete(
        cls, user_id: int, user_service: UserService = Depends(UserService)
    ) -> dict[str, bool]:
        """
        ユーザー削除API

        Args:
            user_id (int): ユーザーID
            user_service (UserService): ユーザーサービス

        Returns:
            dict[str, str]: 削除完了メッセージ
        """

        user_service.delete_user(user_service.get_user(user_id))
        return {"is_deleted": True}
