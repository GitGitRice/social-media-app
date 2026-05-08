from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from .user_model import User, UserRead


class FollowBase(SQLModel):
    """
    Data model with the basic follow attributes.
    """
    # These IDs link the follower and the followed user.
    follower_id: int = Field(foreign_key="user.id", index=True)
    followed_id: int = Field(foreign_key="user.id", index=True)


class Follow(FollowBase, table=True):
    """
    Table model with the columns stored in db.
    """
    id:int | None = Field(default=None, primary_key=True)
       

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    # This constraint ensures the combination of follower and followed is unique,
    # preventing a user from following the same person multiple times.
    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="unique_follower_followed"),
    )
    follower: "User" = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"primaryjoin": "Follow.follower_id==User.id"}
    )
    followed: "User" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"primaryjoin": "Follow.followed_id==User.id"}
    )


class FollowRead(FollowBase):
    """
    A data model with the additional attributes to be returned for a follow relationship.
    """
    created_at: datetime


class FollowReadWithUsers(FollowRead):
    """
    A data model with the additional attributes to be returned for a follow relationship,
    including the full user objects.
    """
    follower: "UserRead" 
    followed: "UserRead"


class FollowCreate(FollowBase):
    """
    A data model for creating a follow relationship.
    """
    pass
