from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from enum import Enum

class UserBase (SQLModel):
    user_name : str = Field(unique=True)
    first_name: str | None = None
    last_name: str | None = None
    bio : str | None = None


class User (UserBase, table=True):
    id: int | None = Field (default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)
    )
    # hashed_password : str


class UserCreate (UserBase):
    # password: str
    pass


class UserRead (UserBase):
    id: int
    created_at: datetime


class UserPatch (SQLModel):
    user_name : str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio : str | None = None
    password: str | None = None


class UserCreateError(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    DATABASE_ERROR = "DATABASE_ERROR"
