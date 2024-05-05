from datetime import datetime

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.now},
    )


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
