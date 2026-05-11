"""
Models package for the social media app.

This package contains all SQLModel and Pydantic models organized by feature.
"""

from .errors_model import ModelError
from .user_model import User, UserBase, UserCreate, UserRead, UserPatch
from .post_model import Post, PostBase, PostCreate, PostRead, PostDetailsRead
from .comment_model import Comment, CommentBase, CommentCreate, CommentRead
from .follow_model import Follow, FollowBase, FollowRead, FollowReadWithUsers, FollowCreate


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

    # Comment models
    "Comment",
    "CommentBase",
    "CommentCreate",
    "CommentRead",
]
