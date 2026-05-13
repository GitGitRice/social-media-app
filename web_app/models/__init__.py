"""
Models package for the social media app.

This package contains all SQLModel and Pydantic models organized by feature.
"""

from .errors_model import ModelError
from .user_model import User, UserBase, UserCreate, UserRead, UserPatch, UserDetailsRead
from .post_model import Post, PostBase, PostCreate, PostRead, PostDetailsRead
from .comment_model import Comment, CommentBase, CommentCreate, CommentRead
from .follow_model import Follow, FollowBase, FollowRead, FollowReadWithUsers, FollowCreate

from .like_model import Like, LikeRead

__all__ = [
    # Errors
    "ModelError",

    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserPatch",
    "UserDetailsRead",

    # Post models
    "Post",
    "PostBase",
    "PostCreate",
    "PostRead",
    "PostDetailsRead",

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

    # Like models
    "LikeRead",
    "Like"
]
