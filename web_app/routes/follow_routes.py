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

    if result == ModelError.VALIDATION_ERROR:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")
    
    if result == ModelError.USER_ID_NOT_FOUND:
        raise HTTPException(status_code=404, detail="User not found.")
        
    if result == ModelError.DATABASE_ERROR:
        # Usually means the unique constraint was hit
        raise HTTPException(status_code=400, detail="Could not follow user. You may already be following them.")
        
    if isinstance(result, ModelError):
        raise HTTPException(status_code=500, detail=ModelError.DATABASE_ERROR)

    return result


@router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def remove_follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Unfollows a specific user by their ID.
    """
    result = unfollow_user(
        session=session, 
        follower_id=current_user.id, 
        followed_id=user_id
    )

    if result == ModelError.FOLLOW_NOT_FOUND:
        raise HTTPException(status_code=404, detail="Follow relationship not found.")
    
    if result == ModelError.DATABASE_ERROR:
        raise HTTPException(status_code=500, detail="Internal database error.")

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