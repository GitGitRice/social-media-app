from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


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
