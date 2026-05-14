from console_app.client_api import get_posts
from .utils import print_header, clear_screen, render_post_panel
from .post_details import post_details_screen
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()

def global_feed_screen():
        while True:
            clear_screen()
            print_header ("Social Media App", "Global Feed")
            
            posts = get_posts()
            if not posts:
                console.print("[yellow]Der Feed ist noch leer.[/yellow]")
            else:
                for post in posts:
                    console.print(render_post_panel(post))
            # Only offer 'Details' if there are actual posts to view
            menu_choices = ["Home"]
            if posts:
                menu_choices.insert(0, "Details")
            
            choice = questionary.select(
                "",
                choices = menu_choices
            ).ask()

            if choice == "Details" and posts:
                selected_post_id = questionary.select(
                    "Select a post ID to see details:",
                    choices = [str(post.id) for post in posts]
                ).ask()
                if selected_post_id:
                    return lambda: post_details_screen(selected_post_id)
                continue

            return "HOME"
