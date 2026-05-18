from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from .comment_model import CommentRead
from .like_model import LikeRead, Like

if TYPE_CHECKING:
    from .comment_model import Comment
    from .user_model import User


class PostBase(SQLModel):
    """
    Data model with the basic post attributes.
    """
    content: str


class Post(PostBase, table=True):
    """
    Table model with the columns stored in db.
    """
    # author_id is the foreign key for User table
    author_id: int = Field(foreign_key="user.id")
    id: int | None = Field(default=None, primary_key=True)
    # index=True for faster requests in the feed
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True
    )

    # Relationship: each post belongs to one author
    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")
    likes: list["Like"] = Relationship(back_populates="post")

    # Additional attributes
    @property
    def comments_count(self) -> int:
        return len(self.comments) if self.comments else 0
    
    @property
    def likes_count(self) -> int:
        return len(self.likes) if self.likes else 0
    

# class PostCreate is not currently needed but could be used later on
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
    comments_count: int
    likes_count: int

    # allows Pydantic to validate SQLAlchemy models and hybrid properties directly by accessing them as object attributes.
    class Config:
        from_attributes = True


class PostDetailsRead(PostRead):
    """
    A data model with nested details for a single post.
    """
    comments: list[CommentRead]
    likes: list[LikeRead]
    comment_count: int = 0
