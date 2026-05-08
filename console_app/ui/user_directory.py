from console_app.constants import UIScreen
from console_app.client_api import get_users
from console_app.state import session
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
import questionary
from .utils import print_header, clear_screen

console = Console()

def user_directory_screen() -> UIScreen:
    """Shows list of all users and provides selection to user details"""

    print_header("Social Media App", "User Directory")
    users = get_users()
    if not users:
        console.print("\n[yellow]No Users found in the database.[/yellow]\n")
        questionary.press_any_key_to_continue().ask()
        return UIScreen.MAIN_MENU

    # 1. Create and Display the Rich Table
    table = Table(title="User Directory", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Username", style="cyan")
    table.add_column("Created At", justify="right")

    for user in users:
        table.add_row(
            str(user.id), 
            user.user_name, 
            user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A"
        )

    console.print(table)

    # 2. Provide Interaction Options
    # We create a list of names for the menu, plus a "Back" option
    user_choices = [user.user_name for user in users]
    
    selection = questionary.select(
        "Select a user to see details or go back:",
        choices=user_choices + [questionary.Separator(), "Back to Main Menu"],
        qmark="",
        instruction=" "
    ).ask()

    # 3. Logic handling
    if selection == "Back to Main Menu" or selection is None:
        return UIScreen.MAIN_MENU
    
    # Find the specific user object that matches the selection
    selected_user = next(u for u in users if u.user_name == selection)
    session.selected_user = selected_user
    return UIScreen.USER_DETAILS