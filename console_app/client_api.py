import httpx
from web_app.models import UserCreate, UserRead, PostCreate, PostRead, UserDetailsRead, PostDetailsRead, CommentCreate
from .state import session
import os

#-------------------------- User --------------------------------- 

def login_user(user_name: str, password: str) -> bool:
    """Uses provided user_name and password to login the user."""
    # FastAPI /token expects 'username' and 'password' in form fields
    login_data = {
        "username": user_name, 
        "password": password
    }
    
    try:
        # Use 'data=' for form-encoding, 'json=' for JSON (FastAPI /token needs 'data=')
        response = session.client.post("/api/token", data=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            
            # Save token to session (this also updates the headers!)
            session.save_token(token)
            
            # Now fetch the user info to fully populate the session
            me_response = session.client.get("/api/users/me")
            if me_response.status_code == 200:
                session.user = me_response.json()
                return True
                
        return False
    except httpx.ConnectError:
        print("Could not connect to the server.")
        return False    

def get_my_user() -> UserRead | None:
    """
    Returns the current user data from the server.
    
    Returns None, if request fails.
    """
    try:
        response = session.client.get("/api/users/me")
        if response.status_code == 200:
            # validate JSON response into UserRead object
            return UserRead.model_validate(response.json())
    except httpx.ConnectError:
        return None

def add_user(user: UserCreate) -> UserRead | None:
    """Sends a UserCreate object and returns a UserRead object."""
    try:
        # .model_dump() turns the Pydantic object into a JSON-serializable dict
        response = session.client.post("/api/users", json=user.model_dump())
        
        if response.status_code == 200:
            return UserRead.model_validate(response.json())
        
        # Log the error detail from FastAPI if something went wrong
        print(f"API Error: {response.json().get('detail')}")
        return None
    except httpx.ConnectError:
        print("Network Error: Could not connect to server.")
        return None

def get_users() -> list[UserDetail]:
    """Returns a list of UserDetail objects."""
    try:
        response = session.client.get("/api/users")
        if response.status_code == 200:
            # validate JSON response into UserRead object
            return [UserDetail.model_validate(u) for u in response.json()]
        return []
    except httpx.ConnectError:
        return []


#--------------------------- Posts ----------------------------

def add_post(post: PostCreate) -> PostRead | None:
    """Sends a new post to the server."""
    try:
        # user_id is handed over as query paramater
        response = session.client.post(
            "/api/posts",
            json=post.model_dump()
        )
        if response.status_code == 200:
            return PostRead.model_validate(response.json())
        return None
    except httpx.ConnectError:
        return None

def get_posts(offset: int = 0, limit: int = 20) -> list[PostRead]:
    """Fetches the global feed."""
    try:
        response = session.client.get("/api/posts", params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except httpx.ConnectError:
        return []
    
def get_post(post_id: int ) -> PostDetailsRead | None:
    """Fetches the details of the specified Post"""
    try:
        response = session.client.get(f"/api/posts/{post_id}")
        if response.status_code == 200:
            return PostDetailsRead.model_validate(response.json())
        return None
    except httpx.ConnectError:
        return None
    
def get_user_posts(user_id: int) -> list[PostRead]:
    """Fetches all posts of a specific user."""
    try:
        response = session.client.get(f"/api/users/{user_id}/posts")
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except httpx.ConnectError:
        return []
    
def remove_post(post_id: int) -> bool:
    """Sends a DELETE request to the server."""
    try:
        response = session.client.delete(f"/api/posts/{post_id}")
        return response.status_code == 200
    except httpx.ConnectError:
        return False
    
def create_comment(post_id: int, comment_content: str) -> bool:
    try:
        comment = CommentCreate (content=comment_content, post_id=post_id)
        response = session.client.post(
            f"/api/posts/{post_id}/comment",
            json=comment.model_dump()    
        )
        return response.status_code == 200
    except httpx.ConnectError:
        return False
        
def toggle_like(post_id):
    try:
        response = session.client.post(f"/api/posts/{post_id}/like")
        if response.status_code == 200:
            return True
    except httpx.ConnectError:
        return False

    #-------------------------- Follows ---------------------------------

def get_user_details(user_id: int) -> UserDetailsRead | None:
    """
    Fetches full user details, including social status (is_following).
    This should be used when rendering the profile screen.
    """
    try:
        response = session.client.get(f"/api/users/{user_id}")
        if response.status_code == 200:
            return UserDetailsRead.model_validate(response.json())
        return None
    except httpx.ConnectError:
        return None

def follow_user(user_id: int) -> bool:
    """Sends a POST request to follow a user."""
    try:
        response = session.client.post(f"/api/users/{user_id}/follow")
        
        if response.status_code == 200:
            return True
        
        # Handle business logic errors (e.g., FOLLOW_EXISTS) by logging the detail.
        # This allows the UI/User to understand why the action failed.
        print(f"Follow failed: {response.json().get('detail', 'Unknown error')}")
        return False
    except httpx.ConnectError:
        return False

def unfollow_user(user_id: int) -> bool:
    """Sends a DELETE request to unfollow a user."""
    try:
        # Our endpoint returns 204 No Content on success
        response = session.client.delete(f"/api/users/{user_id}/follow")
        
        if response.status_code == 204:
            return True
            
        print(f"Unfollow failed: {response.json().get('detail', 'Unknown error')}")
        return False 
    except httpx.ConnectError:
        return False

def check_is_following(user_id: int) -> bool:
    """Checks if the logged-in user is currently following the target user."""
    try:
        response = session.client.get(f"/api/users/{user_id}/is_following")
        if response.status_code == 200:
            return response.json().get("is_following", False)
        return False
    except httpx.ConnectError:
        return False
    

def get_followed_users(user_id: int) -> list[UserRead]:
    """Fetches a list of users the target user follows."""
    try:
        response = session.client.get(f"/api/users/{user_id}/following")
        if response.status_code == 200:
            return [UserRead.model_validate(u) for u in response.json()]
        return []
    except httpx.ConnectError:
        return []

def get_following_posts(offset: int = 0, limit: int = 20) -> list[PostRead]:
    """Fetches the authenticated user's following feed."""
    try:
        response = session.client.get("/api/posts/feed/following", params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            return [PostRead.model_validate(p) for p in response.json()]
        return []
    except httpx.ConnectError:
        return []