from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session

from web_app.database import get_session, engine
from web_app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from web_app.models import UserCreate, ModelError, UserRead, User, PostRead, PostCreate
from web_app.crud import get_user_by_user_name, add_user_to_db, get_users_from_db, create_post, get_posts, get_post_by_id, get_posts_by_user, delete_post_from_db

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


#--------------------------- Post Routes  ----------------------------

# POST /posts (Create Post)
@app.post("/api/posts", response_model=PostRead)
def add_post(
    post: PostCreate, 
    user_id: int, 
    session: Session = Depends(get_session)
    ):
    """
    Accepts a PostCreate object and a user_id to store it to the database.
    """
    return create_post(session, post, user_id)

# GET /posts (Global Feed)
@app.get("/api/posts", response_model=list[PostRead])
def read_posts(
    offset: int = 0, 
    limit: int = 20, 
    session: Session = Depends(get_session)
    ):
    """
    Returns a paginated list of all public posts.
    """
    return get_posts(session, offset, limit)

# GET /posts/{post_id} (Fetch Single Post)
@app.get("/api/posts/{post_id}", response_model=PostRead)
def read_post(
    post_id: int, 
    session: Session = Depends(get_session)
    ):
    """
    Fetches a single post record by its unique ID.
    """
    post = get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# GET /users/{id}/posts (User Profile Posts)
@app.get("/api/users/{user_id}/posts", response_model=list[PostRead])
def read_user_posts(
    user_id: int, 
    session: Session = Depends(get_session)
    ):
    """
    Returns all posts associated with a specific user ID.
    """
    return get_posts_by_user(session, user_id)


@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session)):
    """
    Deletes a specific post record from the database.
    """
    success = delete_post_from_db(session, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    return {"detail": "Post erfolgreich gelöscht"}