from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from web_app.database import engine
from web_app.routes import auth_routes, comment_routes, posts_routes, users_routes, follow_routes



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
app.include_router(auth_routes.router, prefix="/api", tags=["Authentication"])
app.include_router(users_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(posts_routes.router, prefix="/api/posts", tags=["Posts"])
app.include_router(comment_routes.router, prefix="/api/posts", tags=["Comments"])

# Static pages used for public, read-only views linked from email notifications.
app.mount("/static", StaticFiles(directory="web_app/static"), name="static")
app.include_router(follow_routes.router, prefix="/api/users", tags=["Follows"])