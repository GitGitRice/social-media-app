from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User, UserRead


class FollowBase(SQLModel):
    """
    Data model with the basic follow attributes.
    """
    # two primary keys create a Composite Primary Key, making the combination unique and preventing 
    # the database from having a duplicate record where one User follows another User more than once 
    follower_id: int = Field(foreign_key="user.id", primary_key=True)
    followed_id: int = Field(foreign_key="user.id", primary_key=True)


class Follow(FollowBase, table=True):
    """
    Table model with the columns stored in db.
    """
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
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
