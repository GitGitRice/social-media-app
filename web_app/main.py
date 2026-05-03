from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session

from web_app.database import get_session, engine

from web_app.models import UserCreate, ModelError, UserRead, User
from web_app.crud import add_user_to_db, get_users_from_db

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

@app.post("/api/users", response_model=UserRead)
def add_user(
    *,
    user: UserCreate, 
    session: Session = Depends(get_session)) -> UserRead:
    """
    Accepts a UserCreate object and a session to store it to.

    Returns a UserRead object in case of success, otherwise a ModelError enum.
    """
    result = add_user_to_db(user, session)
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

