from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from web_app.database import get_session
from web_app.auth import verify_password, create_access_token
from web_app.models import ModelError, User
from web_app.crud import get_user_by_user_name

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Login for receiving access token.
    """
    # get the user based on username. Result is either the found user or a model error
    result = get_user_by_user_name(form_data.username, session)
    if isinstance(result, ModelError):
        if result == ModelError.USER_NAME_NOT_FOUND:
            raise HTTPException(status_code=400, detail=ModelError.USER_NAME_NOT_FOUND)
        else:
            raise HTTPException(status_code=500, detail=ModelError.DATABASE_ERROR)

    #
    user: User = result
    # verify password and give an error if password and hashed password do not match
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # generate access token based on user id
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
