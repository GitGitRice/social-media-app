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


# POST
def add_post(post: PostCreate, user_id: int) -> PostRead | None:
    """Sendet einen neuen Post an den Server."""
    try:
        # user_id wird als Query-Parameter übergeben
        response = requests.post(
            f"{BASE_URL}/posts", 
            params={"user_id": user_id}, 
            json=post.model_dump()
        )
        if response.status_code == 200:
            return PostRead.model_validate(response.json())
        return None
    except requests.exceptions.ConnectionError:
        return None

def get_posts(offset: int = 0, limit: int = 20) -> list[PostRead]:
    """Holt den globalen Feed."""
    try:
        response = requests.get(f"{BASE_URL}/posts", params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []

def get_user_posts(user_id: int) -> list[PostRead]:
    """Holt alle Posts eines spezifischen Nutzers."""
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}/posts")
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except requests.exceptions.ConnectionError:
        return []