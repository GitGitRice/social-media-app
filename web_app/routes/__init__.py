"""
Routes package for the social media app.

This package contains all API route handlers organized by feature.
"""

from . import auth, users, posts

__all__ = [
    "auth",
    "users",
    "posts",
]
