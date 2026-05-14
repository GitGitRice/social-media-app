from console_app.client_api import get_users
from .utils import print_header, clear_screen, Emoji
from .user_details import user_details_screen
from rich.console import Console
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
    
    # 1. Build multiline choices for the selection menu
    choices = []
    for user in users:
        created_date = user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A"
        
        # Construct a multiline display string based on the colleague's suggestion
        display_text = (
            f"{user.user_name} (ID: {user.id})\n"
            f"   Posts: {user.post_count} | Joined: {created_date}\n"
            f"   Following: {'Yes' if user.is_following else 'No'} | Follows You: {Emoji.LIKE.value if user.follows_you else 'No'}"
        )
        choices.append(questionary.Choice(title=display_text, value=user.id))

    # Add navigation and structural elements
    choices.append(questionary.Separator())
    choices.append(questionary.Choice(title="Back to Main Menu", value="HOME"))
    
    selection = questionary.select(
        "Select a user to see details or go back:",
        choices=choices,
        qmark="",
        instruction=" "
    ).ask()

    if selection == "HOME" or selection is None:
        return "HOME"
    
    return lambda: user_details_screen(selection)