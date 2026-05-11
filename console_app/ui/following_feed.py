from console_app.constants import UIScreen
from console_app.client_api import get_following_posts
from rich.console import Console
from rich.panel import Panel
import questionary
from .utils import print_header, clear_screen

console = Console()

def following_feed_screen() -> UIScreen:
    clear_screen()
    print_header ("Social Media App", "Following Feed")
    
    posts = get_following_posts()
    if not posts:
        console.print("[yellow]No posts found. Try following some users![/yellow]")
    else:
        for post in posts:
            console.print(Panel(post.content, title=f"Post ID: {post.id} (User {post.author_id})"))
    
    questionary.press_any_key_to_continue().ask()
    return UIScreen.MAIN_MENU