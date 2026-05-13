from console_app.client_api import get_users
from .utils import print_header, clear_screen
from .user_details import user_details_screen
from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()

def user_directory_screen():
    """Shows list of all users and provides selection to user details"""
    clear_screen()
    print_header("Social Media App", "User Directory")
    users = get_users()
    if not users:
        console.print("\n[yellow]No Users found in the database.[/yellow]\n")
        questionary.press_any_key_to_continue().ask()
        return "BACK"
    
    # 1. Display each user as a Rich Panel
    for user in users:
        # 'user' is now a UserDetail object containing all counts and social status
        created_date = user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A"
        
        console.print(
            Panel(
                f"[cyan]ID:[/cyan] {user.id}\n"
                f"[cyan]Username:[/cyan] {user.user_name}\n"
                f"[cyan]Created At:[/cyan] {created_date}\n"
                f"[cyan]Posts:[/cyan] {user.post_count}\n"
                f"[cyan]Followed by You:[/cyan] {'Yes' if user.is_following else 'No'}\n"
                f"[cyan]Follows You:[/cyan] {'Yes' if user.follows_you else 'No'}",
                title=f"User: {user.user_name}",
                subtitle=f"ID: {user.id}"
            )
        )

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
        return "HOME"
    
    # Find the specific user object that matches the selection
    selected_user = next(u for u in users if u.user_name == selection)

    return lambda : user_details_screen(selected_user.id) # Pass user_id instead of UserRead object