from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.user_social_account import UserSocialAccount


class UserBase(SQLModel):
    name: str = Field(max_length=255)
    email: str = Field(unique=True, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )

    user_social_accounts: list["UserSocialAccount"] = Relationship(
        back_populates="user"
    )


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserPasswordLogin(SQLModel):
    email: str
    password: str


class Token(SQLModel):
    token_type: str
    access_token: str
