from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from web_app.auth import get_current_user
from web_app.crud import add_comment
from web_app.database import get_session
from web_app.models import CommentBase, CommentRead, ModelError, User, UserRead

router = APIRouter()


@router.post("/{post_id}/comment", response_model=CommentRead)
def create_comment(
    post_id: int,
    comment: CommentBase,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> CommentRead:
    """
    Creates a new comment for a specific post.
    """
    # Validating to UserRead ensures the ID is an int and not None for the type checker
    current_user = UserRead.model_validate(user)

    result = add_comment(
        session=session,
        user_id=current_user.id,
        post_id=post_id,
        content=comment.content,
    )

    if result == ModelError.POST_NOT_FOUND:
        raise HTTPException(status_code=404, detail=ModelError.POST_NOT_FOUND)

    if result == ModelError.USER_ID_NOT_FOUND:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if isinstance(result, ModelError):
        raise HTTPException(status_code=500, detail=ModelError.DATABASE_ERROR)

    return CommentRead.model_validate(result)
