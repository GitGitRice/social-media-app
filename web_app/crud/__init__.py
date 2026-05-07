"""
CRUD package for the social media app.

This package contains all database CRUD operations organized by feature.
"""

from .user import (
    get_user_by_user_name,
    get_user_by_id,
    add_user_to_db,
    get_users_from_db,
)

from .post import (
    create_post,
    get_posts,
    get_post_by_id,
    get_posts_by_user,
    delete_post_from_db,
)

__all__ = [
    # User CRUD
    "get_user_by_user_name",
    "get_user_by_id",
    "add_user_to_db",
    "get_users_from_db",

    # Post CRUD
    "create_post",
    "get_posts",
    "get_post_by_id",
    "get_posts_by_user",
    "delete_post_from_db",
]
