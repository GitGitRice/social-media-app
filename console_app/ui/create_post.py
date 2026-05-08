from console_app.constants import UIScreen
import questionary
from web_app.models import PostCreate
from console_app.client_api import add_post
from rich.console import Console
from .utils import print_header, clear_screen

console = Console()

def create_post_screen() -> UIScreen:
    """
    Enables currently logged in user to post posts.
    """
    clear_screen()
    print_header ("Social Media App", "Create a Post")
    
    content = questionary.text("Was möchtest du teilen?").ask()
    if content:
        post_data = PostCreate(content=content)
        if add_post(post_data):
            console.print("[green]Post erfolgreich veröffentlicht![/green]")
        else:
            console.print("[red]Fehler beim Posten.[/red]")
    return UIScreen.MAIN_MENU