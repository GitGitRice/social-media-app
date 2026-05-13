from console_app.client_api import get_posts
from .utils import print_header, clear_screen, render_post_panel
from .post_details import post_details_screen
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
            console.print(render_post_panel(post))
    
    choice = questionary.select(
        "",
        choices=["Details", "Home"]
    ).ask()

    if choice == "Details":
        selected_post_id = questionary.select(
            "",
            [str(post.id) for post in posts]
        ).ask()

        return lambda: post_details_screen(selected_post_id)
    elif choice == "Home":
        return "HOME"