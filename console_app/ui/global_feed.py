from console_app.client_api import get_posts
from .utils import print_header, clear_screen

from rich.table import Table
from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()

def global_feed_screen():
    clear_screen()
    print_header ("Social Media App", "Global Feed")
    
    posts = get_posts()
    if not posts:
        console.print("[yellow]Der Feed ist noch leer.[/yellow]")
    else:
        for post in posts:
            console.print(Panel(post.content, title=f"Post ID: {post.id} (User {post.author_id})"))
    
    questionary.press_any_key_to_continue().ask()
    return "HOME"