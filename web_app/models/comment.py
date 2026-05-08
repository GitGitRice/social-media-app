from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .post import Post
    from .user import User


class CommentBase(SQLModel):
    """
    Data model with the basic comment attributes.
    """
    content: str


class Comment(CommentBase, table=True):
    """
    Table model with the columns stored in db.
    """
    id: int | None = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")

    user: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")


class CommentCreate(CommentBase):
    """
    Data model with the additional attributes during comment creation.
    """
    post_id: int


class CommentRead(CommentBase):
    """
    A data model with the additional attributes to be returned for a comment.
    """
    id: int
    created: datetime
    user_id: int
    post_id: int
