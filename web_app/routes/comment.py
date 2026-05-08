from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session

from web_app.auth import get_current_user
from web_app.crud import add_comment, get_post_author
from web_app.database import get_session
from web_app.email import send_comment_notification
from web_app.models import CommentBase, CommentRead, ModelError, User

router = APIRouter()


@router.post("/{post_id}/comment", response_model=CommentRead)
def create_comment(
    post_id: int,
    comment: CommentBase,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> CommentRead:
    """
    Creates a new comment for a specific post.
    """
    result = add_comment(
        session=session,
        user_id=user.id,
        post_id=post_id,
        content=comment.content,
    )

    if result == ModelError.POST_NOT_FOUND:
        raise HTTPException(status_code=404, detail=ModelError.POST_NOT_FOUND)

    if result == ModelError.USER_ID_NOT_FOUND:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if isinstance(result, ModelError):
        raise HTTPException(status_code=500, detail=ModelError.DATABASE_ERROR)

    post_author = get_post_author(session, post_id)
    if post_author and post_author.id != user.id:
        background_tasks.add_task(
            send_comment_notification,
            post_author.email,
            post_id,
            user.user_name,
        )

    return CommentRead.model_validate(result)
