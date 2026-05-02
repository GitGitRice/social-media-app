from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session

from web_app.database import get_session, engine

from web_app.models import UserCreate, UserCreateError, UserRead, User
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

    result = add_user_to_db(user, session)
    if isinstance(result, UserCreateError):
        if result == UserCreateError.ALREADY_EXISTS:
            raise HTTPException(status_code=400, detail="Username already taken")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
    return UserRead.model_validate(result)

@app.get("/api/users", response_model=list[UserRead])
def get_users(*, session: Session = Depends(get_session)) -> list[UserRead]:
    users = get_users_from_db(session)
    return [UserRead.model_validate(user) for user in users]

