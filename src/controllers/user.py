from fastapi import HTTPException, Query
from sqlmodel import Session, select

from src.connector.db_connect import engine
from src.models.user import User, UserCreate, UserPublic, UserUpdate


class UserController:
    @classmethod
    async def index(
        cls, offset: int = 0, limit: int = Query(default=100, le=100)
    ) -> list[UserPublic]:
        """
        ユーザー一覧を返すクラスメソッド。

        Args:
            offset (int): 取得開始位置。
            limit (int): 取得件数。

        Returns:
            list[UserPublic]: ユーザー一覧。
        """
        with Session(engine) as session:
            users = session.exec(select(User).offset(offset).limit(limit)).all()

            return [UserPublic.model_validate(user) for user in users]

    @classmethod
    async def show(cls, user_id: int) -> UserPublic | None:
        """
        指定したユーザーIDに対応するユーザー情報を返すクラスメソッド。

        Args:
            user_id (int): ユーザーID。

        Returns:
            UserPublic: ユーザー情報。

        Raises:
            HTTPException: ユーザーが見つからない場合に発生。
        """
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return UserPublic.model_validate(user)

    @classmethod
    async def create(cls, user: UserCreate) -> UserPublic:
        """
        ユーザー情報を登録するクラスメソッド。

        Args:
            user (UserCreate): ユーザー情報。

        Returns:
            UserPublic: 登録したユーザー情報。
        """
        with Session(engine) as session:
            db_user = User.model_validate(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

        return UserPublic.model_validate(db_user)

    @classmethod
    async def update(cls, user_id: int, user: UserUpdate) -> UserPublic:
        """
        ユーザー情報を更新するクラスメソッド。

        Args:
            user_id (int): ユーザーID。
            user (UserUpdate): ユーザー情報。

        Returns:
            UserPublic: 更新したユーザー情報。

        Raises:
            HTTPException: ユーザーが見つからない場合に発生。
        """
        with Session(engine) as session:
            db_user = session.get(User, user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")

            user_data = user.model_dump(exclude_unset=True)
            db_user.sqlmodel_update(user_data)
            session.commit()
            session.refresh(db_user)

        return UserPublic.model_validate(db_user)

    @classmethod
    async def delete(cls, user_id: int) -> dict[str, bool]:
        """
        ユーザー情報を削除するクラスメソッド。

        Args:
            user_id (int): ユーザーID。

        Returns:
            dict[str, str]: 削除完了メッセージ。

        Raises:
            HTTPException: ユーザーが見つからない場合に発生。
        """
        with Session(engine) as session:
            db_user = session.get(User, user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")

            session.delete(db_user)
            session.commit()

        return {"ok": True}
