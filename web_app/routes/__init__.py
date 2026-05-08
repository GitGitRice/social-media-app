"""
Routes package for the social media app.

This package contains all API route handlers organized by feature.
"""

from . import auth_routes, comment_routes, posts_routes, users_routes

__all__ = [
    "auth_routes",
    "users_routes",
    "posts_routes",
    "comment_routes",
]
