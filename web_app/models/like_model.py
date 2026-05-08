from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from .post import Post
    from .user import User

class Like(SQLModel, table=True):

    # database columns
    id: int | None = Field(default=None, primary_key=True) 
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # relationships
    user: User = Relationship(back_populates="likes")
    post: Post = Relationship(back_populates="likes")

    # prevents duplicate likes
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )