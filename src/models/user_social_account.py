from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.user import User


class UserSocialAccount(SQLModel, table=True):
    __tablename__ = "user_social_accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(index=True, default=None, foreign_key="users.id")
    provider: str = Field(max_length=255)
    provider_user_id: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )

    user: Optional[User] = Relationship(back_populates="user_social_accounts")
