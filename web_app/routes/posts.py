from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from web_app.database import get_session
from web_app.auth import get_current_user
from web_app.models import UserRead, User, PostRead, PostCreate, Post
from web_app.crud import create_post, get_posts, get_post_by_id, get_posts_by_user, delete_post_from_db

router = APIRouter()


# POST /posts (Create Post)
@router.post("", response_model=PostRead)
def add_post(
    post: PostCreate,
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

    return create_post(session=session, db_post=db_post)


# GET /posts (Global Feed)
@router.get("", response_model=list[PostRead])
def read_posts(
    offset: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session)
):
    """
    Returns a paginated list of all public posts.
    """
    return get_posts(session, offset, limit)


# GET /posts/{post_id} (Fetch Single Post)
@router.get("/{post_id}", response_model=PostRead)
def read_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """
    Fetches a single post record by its unique ID.
    """
    post = get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session)):
    """
    Deletes a specific post record from the database.
    """
    success = delete_post_from_db(session, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    return {"detail": "Post erfolgreich gelöscht"}
