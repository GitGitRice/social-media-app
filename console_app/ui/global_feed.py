from console_app.client_api import get_posts
from .feed import build_feed_screen_selector
from .utils import print_header, clear_screen
from rich.console import Console
import questionary

console = Console()


def global_feed_screen():

    # clear screen and print header
    clear_screen()
    print_header ("Social Media App", "Global Feed")

    # retrieve posts from server
    posts = get_posts()
    if not posts:
        console.print("[yellow]Feed is empty.[/yellow]")

    return build_feed_screen_selector (posts)
    