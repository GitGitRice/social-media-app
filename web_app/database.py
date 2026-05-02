from sqlmodel import create_engine, Session
import os

# 1. Define the database location
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. Create the Engine
# check_same_thread=False is REQUIRED for SQLite + FastAPI
# because FastAPI can handle requests on different threads.
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    echo=True  # Set to True to see the actual SQL queries in your console
)

# 3. Dependency to be used in FastAPI routes
def get_session():
    """
    Provides a database session that automatically closes 
    after the request is finished.
    """
    with Session(engine) as session:
        yield session