from web_app.models import PostCreate
from console_app.client_api import add_post
from .utils import print_header, clear_screen, print_error, print_success
import questionary
from rich.console import Console

console = Console()

def create_post_screen():
    """
    Enables currently logged in user to post posts.
    """
    clear_screen()
    print_header ("Social Media App", "Create a Post")
    
    content = questionary.text("Was möchtest du teilen?", multiline=True).ask()
    if content:
        post_data = PostCreate(content=content)
        if add_post(post_data):
            print_success("Post created.")
        else:
            print_error("Error creating Post")
    return "HOME"