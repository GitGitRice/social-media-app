from console_app.client_api import get_following_posts
from .utils import print_header, clear_screen

from rich.console import Console
from .feed import build_feed_screen_selector


console = Console()

def following_feed_screen():
    """
    Displays a personalized feed of posts from users the current user follows.
    """
    clear_screen()
    print_header ("Social Media App", "Following Feed")
    
    # Fetch data from the backend client_api
    posts = get_following_posts()

    if not posts:
        console.print("[yellow]Feed is empty.[/yellow]")

    return build_feed_screen_selector (posts)