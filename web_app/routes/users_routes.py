from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from web_app.database import get_session
from web_app.auth import get_password_hash, get_current_user
from web_app.models import UserCreate, ModelError, UserRead, User, PostRead, UserDetail
from web_app.crud import add_user_to_db, get_users_from_db,get_user_by_id, get_posts_by_user, get_posts_by_user, get_followers_for_user, get_followed_users, is_following

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_my_user(
    *,
    user: User = Depends(get_current_user)
) -> UserRead:

    return UserRead.model_validate(user)


@router.post("", response_model=UserRead)
def add_user(
    *,
    user: UserCreate,
    session: Session = Depends(get_session)) -> UserRead:
    """
    Accepts a UserCreate object and a session to store it to.

    Returns a UserRead object in case of success, otherwise a ModelError enum.
    """

    # obtains password from UserCreate, hashes it and stores the hash in User
    hashed_pwd: str = get_password_hash(user.password)
    user_data = user.model_dump(exclude={"password"})
    db_user = User(**user_data, hashed_password=hashed_pwd)

    result = add_user_to_db(db_user, session)
    if isinstance(result, ModelError):
        if result == ModelError.USER_NAME_ALREADY_EXISTS:
            raise HTTPException(status_code=400, detail=ModelError.USER_NAME_ALREADY_EXISTS)
        else:
            raise HTTPException(status_code=500, detail=ModelError.DATABASE_ERROR)
    return UserRead.model_validate(result)


@router.get("", response_model=list[UserRead])
def get_users(
    *, 
    user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
) -> list[UserRead]:
    """
    Returns a list of UserRead objects.

    TODO: No error handling.
    """
    users = get_users_from_db(session)
    if isinstance(users, ModelError):
        raise HTTPException(status_code=500, detail=ModelError.DATABASE_ERROR)
    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserDetail)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Returns the detailed profile of a specific user.
    Aggregates data from user_crud and follow_crud to satisfy the UserDetail model.
    """
    db_user = get_user_by_id(user_id, session)
    if isinstance(db_user, ModelError):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create the detailed model base
    user_detail = UserDetail.model_validate(db_user)
    
    # Enrich with social data from follow_crud.py
    user_detail.followers_count = len(get_followers_for_user(session, user_id))
    user_detail.following_count = len(get_followed_users(session, user_id))
    user_detail.is_following = is_following(session, current_user.id, user_id)
    
    return user_detail


@router.get("/{user_id}/posts", response_model=list[PostRead])
def read_user_posts(
    user_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Returns all posts associated with a specific user ID.
    """
    return get_posts_by_user(session, user_id)
