from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .follow import Follow


class UserBase(SQLModel):
    """
    A data model with the basic user attributes.
    """
    user_name: str = Field(unique=True)
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


class User(UserBase, table=True):
    """
    A table model with the columns stored in db.
    """
    id: int | None = Field(default=None, primary_key=True) # need to be optional due to SQLModel inner workings.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hashed_password: str
    posts: list["Post"] = Relationship(back_populates="author")

    # Relationships for following/followers
    following: list["Follow"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"primaryjoin": "User.id==Follow.follower_id"}
    )
    followers: list["Follow"] = Relationship(
        back_populates="followed",
        sa_relationship_kwargs={"primaryjoin": "User.id==Follow.followed_id"}
    )


class UserCreate(UserBase):
    """
    A data model with the additional attributes during user creation.
    """
    password: str
    pass


class UserRead(UserBase):
    """
    A data model with the additonal attributes to be returned for a user.
    """
    id: int
    created_at: datetime


class UserPatch(SQLModel):
    """
    A data model with the attributes to be used for PATCH routes.
    """
    user_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    password: str | None = None


class UserDetail(UserRead):
    is_following: bool = False
