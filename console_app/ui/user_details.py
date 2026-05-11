from console_app.constants import UIScreen
from console_app.state import session
from console_app.client_api import follow_user, unfollow_user, check_is_following, get_followed_users
from .utils import print_error, print_header, clear_screen, print_success, pause
from rich.panel import Panel
from rich.console import Console
import questionary


console = Console()

def user_details_screen() -> UIScreen:
    """Displays detailed information about a single user and Follow actions."""
    clear_screen()
    print_header("Social Media App", "User Details")
    
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
    
    # Check if the logged-in user is viewing their own profile
    is_own_profile = session.user and session.user.get("id") == session.selected_user.id
    choices = ["Back"]
    
    if not is_own_profile:
        is_following = check_is_following(session.selected_user.id)
        if is_following:
            choices.insert(0, "Unfollow")
        else:
            choices.insert(0, "Follow")
    else:
        # If it is my own profile, add the "View Following" option
        choices.insert(0, "View Following")
            
    action = questionary.select("Actions:", choices=choices).ask()

    # Handle menu actions
    if action == "Follow":
        if follow_user(session.selected_user.id):
            print_success(f"You are now following {session.selected_user.user_name}!")
        else:
            print_error("Could not follow user.")
        return UIScreen.USER_DETAILS # Reload screen to update Follow -> Unfollow
        
    elif action == "Unfollow":
        if unfollow_user(session.selected_user.id):
            print_success(f"You unfollowed {session.selected_user.user_name}.")
        else:
            print_error("Could not unfollow user.")
        return UIScreen.USER_DETAILS # Reload screen to update Unfollow -> Follow
    
    if action == "View Following":
        following_list = get_followed_users(session.selected_user.id)
        if not following_list:
            console.print("\n[yellow]You are not following anyone yet.[/yellow]\n")
        else:
            console.print("\n[bold magenta]Users you follow:[/bold magenta]")
            for u in following_list:
                console.print(f"- {u.user_name}")
            print("\n")
        pause()
        return UIScreen.USER_DETAILS

    return UIScreen.USER_DIRECTORY