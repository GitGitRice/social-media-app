from .utils import print_header, clear_screen
from web_app.models import UserRead
from rich.panel import Panel
from rich.console import Console
import questionary

console = Console()

def user_details_screen(selected_user: UserRead):
    """Displays detailed information about a single user."""
    clear_screen()
    print_header ("Social Media App", "User Details")
    
    detail_content = (
        f"[bold]Username:[/bold] {selected_user.user_name}\n"
        f"[bold]First Name:[/bold] {selected_user.first_name or 'N/A'}\n"
        f"[bold]Last Name:[/bold] {selected_user.last_name or 'N/A'}\n"
        f"[bold]Bio:[/bold] {selected_user.bio or 'No biography provided.'}\n"
        f"[bold]Created:[/bold] {selected_user.created_at}"
    )
    
    console.print(Panel(detail_content, title=f"User Profile: {selected_user.user_name}", expand=False))
    
    action = questionary.select(
            "Aktionen:",
            choices=["Back"]
        ).ask()

    return "BACK"
        