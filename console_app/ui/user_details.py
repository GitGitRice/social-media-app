from console_app.state import session
from console_app.client_api import follow_user, unfollow_user, get_followed_users, get_user_details, get_followers
from .utils import print_error, print_header, clear_screen, print_success, pause
from web_app.models import UserDetailsRead
from rich.panel import Panel
from rich.console import Console
import questionary

console = Console()

def user_details_screen(user_id: int): # Changed signature to accept user_id
    """Displays detailed information about a single user and Follow actions."""
    clear_screen()
    print_header("Social Media App", "User Details")
    
    # Fetch the UserDetail directly using the user_id
    user_detail: UserDetailsRead | None = get_user_details(user_id)
    
    if not user_detail:
        # If we cannot fetch the detailed profile, we shouldn't attempt to show Follow actions.
        print_error("Could not fetch user profile details.")
        return "BACK" # Go back to user directory if details can't be fetched
    
    detail_content = (
        f"[bold]Username:[/bold] {user_detail.user_name}\n" # Use user_detail
        f"[bold]First Name:[/bold] {user_detail.first_name or 'N/A'}\n"
        f"[bold]Last Name:[/bold] {user_detail.last_name or 'N/A'}\n"
        f"[bold]Bio:[/bold] {user_detail.bio or 'No biography provided.'}\n"
        f"[bold]Created:[/bold] {user_detail.created_at.strftime('%Y-%m-%d %H:%M')}" # Format datetime
    )
    
    console.print(Panel(detail_content, title=f"User Profile: {user_detail.user_name}", expand=False))
    
    # Check if the logged-in user is viewing their own profile
    # session.user is a dict from the API response, so .get("id") is appropriate
    is_own_profile = session.user and session.user.get("id") == user_detail.id
    choices = ["Back"]
    
    if not is_own_profile:
        if user_detail.is_following: # Use user_detail.is_following
            choices.insert(0, "Unfollow")
        else:
            choices.insert(0, "Follow")
    else:
        # If it is my own profile, add the "View Following" option
        choices.insert(0, "View Following")
            
    action = questionary.select("Actions:", choices=choices).ask()

    # Handle user cancelling the selection (Ctrl+C) or choosing Back
    if action is None or action == "Back": # Go back to user directory
        return "BACK"

    # Handle menu actions
    if action == "Follow":
        if follow_user(user_detail.id): # Use user_detail.id
            print_success(f"You are now following {user_detail.user_name}!")
        else:
            # print_error provides a pause, ensuring the user sees the specific 
            # backend error (e.g., ALREADY_FOLLOWING) before the screen reloads.
            print_error("Follow action failed.")
        return lambda: user_details_screen(user_id) # Reload current screen
        
    elif action == "Unfollow":
        if unfollow_user(user_detail.id): # Use user_detail.id
            print_success(f"You unfollowed {user_detail.user_name}.")
        else:
            print_error("Could not unfollow user.")
        return lambda: user_details_screen(user_id) # Reload current screen
    
    if action == "View Following":
        following_list = get_followed_users(user_detail.id) # Use user_detail.id
        followers_list = get_followers(user_detail.id)

        console.print("\n[bold magenta]Social Connections:[/bold magenta]")

        console.print("\n[cyan]Following:[/cyan]")
        if not following_list:
            console.print("  [dim]You are not following anyone yet.[/dim]")
        else:
            for u in following_list:
                console.print(f"  - {u.user_name}")

        console.print("\n[cyan]Followers:[/cyan]")
        if not followers_list:
            console.print("  [dim]No one is following you yet.[/dim]")
        else:
            for u in followers_list:
                console.print(f"  - {u.user_name}")

        print("\n")
        pause() # Pause to allow user to read the list
        return lambda: user_details_screen(user_id) # Reload current screen

    return "BACK"
        