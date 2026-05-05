from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum


class PostBase(SQLModel):
    content: str
    # author_id ist der Fremdschlüssel zum User
    author_id: int | None = Field(default=None, foreign_key="user.id")

class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # index=True für schnellere Abfragen beim Feed
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        index=True
    )
    
    # Relationship: Ein Post gehört zu einem Autor
    author: "User" = Relationship(back_populates="posts")


class UserBase (SQLModel):
    """
    A data model with the basic user attributes.
    """
    user_name : str = Field(unique=True)
    first_name: str | None = None
    last_name: str | None = None
    bio : str | None = None


class User (UserBase, table=True):
    """
    A table model with the columns stored in db.
    """
    id: int | None = Field (default=None, primary_key=True) # need to be optional due to SQLModel inner workings.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)
    )
    # hashed_password : str
    posts: list["Post"] = Relationship(back_populates="author")


class UserCreate (UserBase):
    """
    A data model with the additional attributes during user creation.
    """
    # password: str
    pass


class UserRead (UserBase):
    """
    A data model with the additonal attributes to be returned for a user.
    """
    id: int
    created_at: datetime


class UserPatch (SQLModel):
    """
    A data model with the attributes to be used for PATCH routes.
    """
    user_name : str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio : str | None = None
    password: str | None = None


class ModelError(str, Enum):
    """
    Collects the different error codes when working with table models.
    """
    VALIDATION_ERROR = "VALIDATION_ERROR" #errors caused by Pydantic evaluation.
    USER_NAME_ALREADY_EXISTS = "USER_NAME_ALREADY_EXISTS"
    DATABASE_ERROR = "DATABASE_ERROR"

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    created_at: datetime