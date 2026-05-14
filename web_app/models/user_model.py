from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .comment_model import Comment
    from .post_model import Post
    from .follow_model import Follow
    from .like_model import Like


class UserBase(SQLModel):
    """
    A data model with the basic user attributes.
    """
    user_name: str = Field(unique=True)
    email: str = Field(unique=True, index=True)
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
    comments: list["Comment"] = Relationship(back_populates="user")
    likes: list["Like"] = Relationship(back_populates="user")

    # Relationships for following/followers
    following: list["Follow"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"primaryjoin": "User.id==Follow.follower_id"}
    )
    followers: list["Follow"] = Relationship(
        back_populates="followed",
        sa_relationship_kwargs={"primaryjoin": "User.id==Follow.followed_id"}
    )

    @property
    def post_count(self) -> int:
        return len(self.posts) if self.posts else 0

    @property
    def followers_count(self) -> int:
        return len(self.followers) if self.followers else 0

    @property
    def following_count(self) -> int:
        return len(self.following) if self.following else 0


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
    followers_count: int = 0
    following_count: int = 0
    post_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class UserPatch(SQLModel):
    """
    A data model with the attributes to be used for PATCH routes.
    """
    user_name: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    password: str | None = None
   


class UserDetailsRead(UserRead):
    """
    Enriches UserRead with relationship status relative to the requester.
    """
    is_following: bool = False  # TODO ask wether this part should be in UserRead or UserDetail, since it is only relevant for the user directory and user details screens, but not for the followers/following screens.
    follows_you: bool = False
    post_count: int = 0
