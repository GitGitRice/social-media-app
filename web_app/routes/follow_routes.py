from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from web_app.auth import get_current_user
from web_app.database import get_session
from web_app.models import ModelError, User, FollowRead, UserRead
from web_app.crud import follow_user, unfollow_user, is_following, get_followed_users, get_followers_for_user


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
    # Narrow the type so Pylance knows the ID is not None
    auth_user = UserRead.model_validate(current_user)
    
    result = follow_user(
        session=session, 
        follower_id=auth_user.id, 
        followed_id=user_id
    )

    if isinstance(result, ModelError):
        # Use .value to provide the consistent error string (e.g., "ALREADY_FOLLOWING")
        raise HTTPException(status_code=result.http_status, detail=result.value)

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
    auth_user = UserRead.model_validate(current_user)

    result = unfollow_user(
        session=session, 
        follower_id=auth_user.id, 
        followed_id=user_id
    )

    if isinstance(result, ModelError):
        # Standardized error reporting
        raise HTTPException(status_code=result.http_status, detail=result.value)

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
    auth_user = UserRead.model_validate(current_user)

    following = is_following(session, auth_user.id, user_id) 
    return {"is_following": following}


@router.get("/{user_id}/following", response_model=list[UserRead])
def read_followed_users(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Fetches the list of users that the specified user follows."""
    return get_followed_users(session, user_id)

@router.get("/{user_id}/followers", response_model=list[UserRead])
def read_followers(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Fetches the list of users that follow the specified user."""
    return get_followers_for_user(session, user_id)