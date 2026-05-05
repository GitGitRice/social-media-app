import requests
from web_app.models import UserCreate, UserRead, PostCreate, PostRead

BASE_URL = "http://127.0.0.1:8000/api"

def add_user(user: UserCreate) -> UserRead | None:
    """Sends a UserCreate object and returns a UserRead object."""
    try:
        # .model_dump() turns the Pydantic object into a JSON-serializable dict
        response = requests.post(f"{BASE_URL}/users", json=user.model_dump())
        
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
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            # validate JSON response into UserRead object
            return [UserRead.model_validate(u) for u in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []
    

def add_post(post: PostCreate) -> PostRead | None:
    """Sendet einen neuen Post an den Server."""
    try:
        response = requests.post(f"{BASE_URL}/posts", json=post.model_dump())
        if response.status_code == 200:
            return PostRead.model_validate(response.json())
        print(f"API Error: {response.json().get('detail')}")
        return None
    except requests.exceptions.ConnectionError:
        print("Network Error: Could not connect to server.")
        return None

def get_posts(offset: int = 0, limit: int = 10) -> list[PostRead]:
    """Holt den globalen Feed."""
    try:
        response = requests.get(f"{BASE_URL}/posts", params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []

def get_posts_by_user(user_id: int, offset: int = 0, limit: int = 10) -> list[PostRead]:
    """Holt alle Posts eines spezifischen Users."""
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}/posts", params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []