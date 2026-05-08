import json
import os
import httpx
from dotenv import load_dotenv
from web_app.models import UserRead

load_dotenv()

class AppSession:
    """
    Manages the http session, the token and the data of the logged in user. 
    """
    def __init__(self):
        self.token_file = ".session.json"
        self.user = None  # Stores the /users/me object
        self.token = None
        self.client = httpx.Client(base_url=os.getenv("SERVER_URL", "http://127.0.0.1:8000"))

        self.selected_user: UserRead | None = None # user selected for user_details_screen

    def save_token(self, token: str) -> None:
        self.token = token
        # Update the HTTP client headers for all future requests
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        with open(self.token_file, "w") as f:
            json.dump({"access_token": token}, f)

    def load_token(self) -> str | None:
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                data = json.load(f)
                self.token = data.get("access_token")
                self.client.headers.update({"Authorization": f"Bearer {self.token}"})
                return self.token
        return None

    def logout(self) -> None:
        self.token = None
        self.user = None
        if os.path.exists(self.token_file):
            os.remove(self.token_file)

session = AppSession()