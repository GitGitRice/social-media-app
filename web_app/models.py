from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum


#--------------------------- User Models ----------------------------
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hashed_password : str
    posts: list["Post"] = Relationship(back_populates="author")



class UserCreate (UserBase):
    """
    A data model with the additional attributes during user creation.
    """
    password: str
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


#--------------------------- Model Errors ----------------------------

class ModelError(str, Enum):
    """
    Collects the different error codes when working with table models.
    """
    VALIDATION_ERROR = "VALIDATION_ERROR" #errors caused by Pydantic evaluation.
    DATABASE_ERROR = "DATABASE_ERROR" # general database errors

    # Errors related to user CRUD
    USER_NAME_ALREADY_EXISTS = "USER_NAME_ALREADY_EXISTS"
    USER_NAME_NOT_FOUND = "USER_NAME_NOT_FOUND"
    USER_ID_NOT_FOUND = "USER_ID_NOT_FOUND"

    # Errors related to post CRUD
    POST_NOT_FOUND = "POST_NOT_FOUND"
    AUTHOR_NOT_FOUND = "AUTHOR_NOT_FOUND" # In case author_id is invalid

#--------------------------- Post Models ----------------------------

class PostBase(SQLModel):
    """
    Data model with the basic post attributes.
    """
    content: str
    # author_id is the foreign key for User table


class Post(PostBase, table=True):
    """
    Table model with the columns stored in db.
    """
    author_id: int = Field(foreign_key="user.id")
    id: int | None = Field(default=None, primary_key=True)
    # index=True for faster requests in the feed
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        index=True
    )
    
    # Relationship: each post belongs to one author
    author: "User" = Relationship(back_populates="posts")

class PostCreate(PostBase):
    """
    Data model with the additional attributes during post creation.
    """
    pass

class PostRead(PostBase):
    """
    A data model with the additional attributes to be returned for a post.
    """
    author_id: int 
    id: int
    created_at: datetime