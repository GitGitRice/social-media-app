from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session

from web_app.database import get_session
from web_app.auth import get_current_user
from web_app.email import send_new_post_notification
from web_app.models import UserRead, User, PostRead, PostCreate, Post, PostDetailsRead, CommentRead, ModelError
from web_app.crud import (
    create_post,
    get_posts,
    get_post_by_id,
    get_posts_by_user,
    delete_post_from_db,
    get_comments_for_post,
    get_followers_for_user,
    toggle_like_on_post
)

router = APIRouter()


# POST /posts (Create Post)
@router.post("", response_model=PostRead)
def add_post(
    post: PostCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Accepts a PostCreate object and a user_id to store it to the database.
    """
    post_data = post.model_dump()
    x: UserRead = UserRead.model_validate(user)
    db_post = Post(**post_data, author_id=x.id)

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    result = create_post(session=session, db_post=db_post)
    if isinstance(result, Post):
        if not user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=ModelError.USER_ID_NOT_FOUND)
        if not result.id:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ModelError.POST_ID_NOT_FOUND)
        for follower in get_followers_for_user(session, user.id):
            background_tasks.add_task(
                send_new_post_notification,
                follower.email,
                result.id,
                user.user_name,
            )

    return result


# GET /posts (Global Feed)
@router.get("", response_model=list[PostRead])
def read_posts(
    offset: int = 0,
    limit: int = 20,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Returns a paginated list of all public posts.
    """
    return get_posts(session, offset, limit)

@router.post("/{post_id}/like")
def toggle_like(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    """
    Toggles the like status of the current_user on the post with post_id.

    Returns the new status of the like.
    """

    if not current_user.id:
        raise HTTPException(status_code=404, detail=ModelError.USER_ID_NOT_FOUND)
    result = toggle_like_on_post(current_user.id, post_id, session)
    if isinstance(result, ModelError):
        raise HTTPException(status_code=result.http_status, detail=result.value)

    return {"is_liked": result, "post_id": post_id}

# GET /posts/{post_id} (Fetch Single Post)
@router.get("/{post_id}", response_model=PostDetailsRead)
def read_post(
    post_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Fetches a single post record by its unique ID.
    """
    post = get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_details = PostDetailsRead.model_validate(post)
    post_details.comments = [
        CommentRead.model_validate(comment)
        for comment in get_comments_for_post(session, post_id)
    ]
    return post_details


@router.delete("/{post_id}")
def delete_post(
    post_id: int, 
    user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """
    Deletes a specific post record from the database.
    """
    success = delete_post_from_db(session, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    return {"detail": "Post erfolgreich gelöscht"}
