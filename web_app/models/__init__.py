"""
Models package for the social media app.

This package contains all SQLModel and Pydantic models organized by feature.
"""

from .errors import ModelError
from .user import User, UserBase, UserCreate, UserRead, UserPatch
from .post import Post, PostBase, PostCreate, PostRead, PostDetailsRead
from .comment import Comment, CommentBase, CommentCreate, CommentRead
from .follow import Follow, FollowBase, FollowRead, FollowReadWithUsers, FollowCreate

__all__ = [
    # Errors
    "ModelError",

    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserPatch",

    # Post models
    "Post",
    "PostBase",
    "PostCreate",
    "PostRead",

    # Follow models
    "Follow",
    "FollowBase",
    "FollowRead",
    "FollowReadWithUsers",
    "FollowCreate",
    "PostDetailsRead",

    # Comment models
    "Comment",
    "CommentBase",
    "CommentCreate",
    "CommentRead",
]
