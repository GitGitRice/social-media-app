"""
CRUD package for the social media app.

This package contains all database CRUD operations organized by feature.
"""

from .user_crud import (
    get_user_by_user_name,
    get_user_by_id,
    add_user_to_db,
    get_users_from_db,
    get_followers_for_user
)

from .post_crud import (
    create_post,
    get_posts,
    get_post_by_id,
    get_post_author,
    get_posts_by_user,
    delete_post_from_db,
    get_following_posts,
    toggle_like_on_post
)

from .comment_crud import (
    add_comment,
    get_comments_for_post,
    get_comment_count,
)

from .follow_crud import (
    follow_user,
    unfollow_user,
    get_follow_relationship,
    is_following,
    get_followed_users,
)

__all__ = [
    # User CRUD
    "get_user_by_user_name",
    "get_user_by_id",
    "add_user_to_db",
    "get_users_from_db",
    "get_followers_for_user",

    # Post CRUD
    "create_post",
    "get_posts",
    "get_post_by_id",
    "get_post_author",
    "get_posts_by_user",
    "delete_post_from_db",
    "get_following_posts",

    "toggle_like_on_post",

    # Comment CRUD
    "add_comment",
    "get_comments_for_post",
    "get_comment_count",

    # Follow CRUD
    "follow_user",
    "unfollow_user",
    "get_follow_relationship",
    "is_following",
    "get_followed_users",
]
