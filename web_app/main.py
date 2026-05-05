from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session

from web_app.database import get_session, engine

from web_app.models import UserCreate, ModelError, UserRead, User, PostRead, PostCreate
from web_app.crud import add_user_to_db, get_users_from_db, create_post, get_posts, get_post_by_id, get_posts_by_user

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


# POST /posts (Create Post)
@app.post("/api/posts", response_model=PostRead)
def add_post(post: PostCreate, user_id: int, session: Session = Depends(get_session)):
    return create_post(session, post, user_id)

# GET /posts (Global Feed)
@app.get("/api/posts", response_model=list[PostRead])
def read_posts(offset: int = 0, limit: int = 20, session: Session = Depends(get_session)):
    return get_posts(session, offset, limit)

# GET /posts/{post_id} (Fetch Single Post)
@app.get("/api/posts/{post_id}", response_model=PostRead)
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# GET /users/{id}/posts (User Profile Posts)
@app.get("/api/users/{user_id}/posts", response_model=list[PostRead])
def read_user_posts(user_id: int, session: Session = Depends(get_session)):
    return get_posts_by_user(session, user_id)