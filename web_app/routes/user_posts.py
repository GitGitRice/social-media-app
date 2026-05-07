from fastapi import APIRouter, Depends
from sqlmodel import Session

from web_app.database import get_session
from web_app.models import PostRead
from web_app.crud import get_posts_by_user

router = APIRouter()


# GET /users/{id}/posts (User Profile Posts)
@router.get("/{user_id}/posts", response_model=list[PostRead])
def read_user_posts(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Returns all posts associated with a specific user ID.
    """
    return get_posts_by_user(session, user_id)
