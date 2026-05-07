from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# load URL from environment variable
db_url = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Create the Engine
# check_same_thread is only needed for SQLite.
connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    db_url, 
    connect_args=connect_args,
# echo = True prints all SQL commands it executes into the terminal. Set to False in production environment
    echo=True 
)

# Dependency used for routes
def get_session():
    with Session(engine) as session:
        yield session