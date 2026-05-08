from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from web_app.database import engine
from web_app.routes import auth, users, posts, comment


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


# Register routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(comment.router, prefix="/api/posts", tags=["Comments"])
