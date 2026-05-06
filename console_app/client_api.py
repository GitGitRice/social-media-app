import requests
from web_app.models import UserCreate, UserRead, PostCreate, PostRead
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# read server url from environment variables
SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8000/api")

def add_user(user: UserCreate) -> UserRead | None:
    """Sends a UserCreate object and returns a UserRead object."""
    try:
        # .model_dump() turns the Pydantic object into a JSON-serializable dict
        response = requests.post(f"{SERVER_URL}/users", json=user.model_dump())
        
        if response.status_code == 200:
            return UserRead.model_validate(response.json())
        
        # Log the error detail from FastAPI if something went wrong
        print(f"API Error: {response.json().get('detail')}")
        return None
    except requests.exceptions.ConnectionError:
        print("Network Error: Could not connect to server.")
        return None

def get_users() -> list[UserRead]:
    """Returns a list of UserRead objects."""
    try:
        response = requests.get(f"{SERVER_URL}/users")
        if response.status_code == 200:
            # validate JSON response into UserRead object
            return [UserRead.model_validate(u) for u in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []


#--------------------------- Posts ----------------------------
def add_post(post: PostCreate, user_id: int) -> PostRead | None:
    """Sends a new post to the server."""
    try:
        # user_id is handed over as query paramater
        response = requests.post(
            f"{SERVER_URL}/posts", 
            params={"user_id": user_id}, 
            json=post.model_dump()
        )
        if response.status_code == 200:
            return PostRead.model_validate(response.json())
        return None
    except requests.exceptions.ConnectionError:
        return None

def get_posts(offset: int = 0, limit: int = 20) -> list[PostRead]:
    """Fetches the global feed."""
    try:
        response = requests.get(f"{SERVER_URL}/posts", params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []

def get_user_posts(user_id: int) -> list[PostRead]:
    """Fetches all posts of a specific user."""
    try:
        response = requests.get(f"{SERVER_URL}/users/{user_id}/posts")
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []
    
def remove_post(post_id: int) -> bool:
    """Sends a DELETE request to the server."""
    try:
        response = requests.delete(f"{SERVER_URL}/posts/{post_id}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False