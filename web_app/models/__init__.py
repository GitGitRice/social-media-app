"""
Models package for the social media app.

This package contains all SQLModel and Pydantic models organized by feature.
"""

from .errors import ModelError
from .user import User, UserBase, UserCreate, UserRead, UserPatch
from .post import Post, PostBase, PostCreate, PostRead

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
]
