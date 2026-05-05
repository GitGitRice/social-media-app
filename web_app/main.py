from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session

from web_app.database import get_session, engine
from web_app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from web_app.models import UserCreate, ModelError, UserRead, User
from web_app.crud import get_user_by_user_name, add_user_to_db, get_users_from_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    # Create tables if they don't exist
    SQLModel.metadata.create_all(engine)
    
    yield  # The app runs while this is "yielded"
    
    # --- Shutdown Logic ---
    # (e.g., closing a connection pool or clearing a cache)
    pass


app = FastAPI(
    title="API for Social Media App",
    version="1.0.0",
    lifespan=lifespan)


@app.post("/api/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Login for receiving access token.
    """
    # get the user based on username. Result is either the found user or a model error
    result = get_user_by_user_name (form_data.username, session)
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

@app.get("/api/users/me", response_model=UserRead)
def get_my_user (
    *, 
    user: User = Depends(get_current_user)
) -> UserRead:
    
    return UserRead.model_validate (user)

@app.post("/api/users", response_model=UserRead)
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

@app.get("/api/users", response_model=list[UserRead])
def get_users(*, session: Session = Depends(get_session)) -> list[UserRead]:
    """
    Returns a list of UserRead objects.

    TODO: No error handling.
    """
    users = get_users_from_db(session)
    return [UserRead.model_validate(user) for user in users]

