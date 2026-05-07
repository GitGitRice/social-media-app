from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from web_app.database import get_session
from web_app.auth import get_password_hash, get_current_user
from web_app.models import UserCreate, ModelError, UserRead, User
from web_app.crud import add_user_to_db, get_users_from_db

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
def get_users(*, session: Session = Depends(get_session)) -> list[UserRead]:
    """
    Returns a list of UserRead objects.

    TODO: No error handling.
    """
    users = get_users_from_db(session)
    return [UserRead.model_validate(user) for user in users]
