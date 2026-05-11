from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from web_app.auth import get_current_user
from web_app.database import get_session
from web_app.models import ModelError, User, FollowRead, UserRead
from web_app.crud import follow_user, unfollow_user, is_following, get_followed_users


router = APIRouter()

@router.post("/{user_id}/follow", response_model=FollowRead)
def create_follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Follows a specific user by their ID.
    """
    # current_user.id is guaranteed to be an int when authenticated
    follower_id = current_user.id
    
    result = follow_user(
        session=session, 
        follower_id=follower_id, 
        followed_id=user_id
    )

    if isinstance(result, ModelError):
        # Format the Enum name for a better frontend error message
        detail_message = str(result.value).replace("_", " ").title() # Convert "CAN_NOT_FOLLOW_YOURSELF" to "Can Not Follow Yourself"
        if result == ModelError.ALREADY_FOLLOWING:
            detail_message = "You are already following this user."
        raise HTTPException(status_code=result.http_status, detail=detail_message)

    return result


@router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def remove_follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Unfollows a specific user by their ID.
    Returns 204 No Content on success.
    """
    result = unfollow_user(
        session=session, 
        follower_id=current_user.id, 
        followed_id=user_id
    )

    if isinstance(result, ModelError):
        detail_message = str(result.value).replace("_", " ").title()
        raise HTTPException(status_code=result.http_status, detail=detail_message)

    return

@router.get("/{user_id}/is_following")
def check_follow_status(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Returns true if the logged-in user follows the target user.
    """
    following = is_following(session, current_user.id, user_id)
    return {"is_following": following}


@router.get("/{user_id}/following", response_model=list[UserRead])
def read_followed_users(
    user_id: int,
    session: Session = Depends(get_session)
):
    """Fetches the list of users that the specified user follows."""
    return get_followed_users(session, user_id)