from console_app.constants import UIScreen
from console_app.state import session
from .utils import print_error
from rich.panel import Panel
from rich.console import Console
import questionary
from .utils import print_header, clear_screen

console = Console()

def user_details_screen() -> UIScreen:
    """Displays detailed information about a single user."""
    clear_screen()
    print_header ("Social Media App", "User Details")
    
    if not session.selected_user:
        print_error("Error in Session: Cannot access selected_user.")
        return UIScreen.USER_DIRECTORY
    
    detail_content = (
        f"[bold]Username:[/bold] {session.selected_user.user_name}\n"
        f"[bold]First Name:[/bold] {session.selected_user.first_name or 'N/A'}\n"
        f"[bold]Last Name:[/bold] {session.selected_user.last_name or 'N/A'}\n"
        f"[bold]Bio:[/bold] {session.selected_user.bio or 'No biography provided.'}\n"
        f"[bold]Created:[/bold] {session.selected_user.created_at}"
    )
    
    console.print(Panel(detail_content, title=f"User Profile: {session.selected_user.user_name}", expand=False))
    
    action = questionary.select(
            "Aktionen:",
            choices=["Back"]
        ).ask()

    return UIScreen.USER_DIRECTORY
        