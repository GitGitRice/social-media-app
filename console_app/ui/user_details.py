from console_app.state import session
from console_app.client_api import follow_user, unfollow_user, get_followed_users, get_user_details, get_followers
from .utils import print_error, print_header, clear_screen, print_success, pause
from web_app.models import UserDetailsRead
from rich.panel import Panel
from rich.console import Console, Group
from rich.table import Table
import questionary

console = Console()

def user_details_screen(user_id: int): # Changed signature to accept user_id
    """Displays detailed information about a single user and Follow actions."""
    while True:
        clear_screen()
        print_header("Social Media App", "User Details")
        
        # Fetch the UserDetail directly using the user_id
        user_detail: UserDetailsRead | None = get_user_details(user_id)
        
        if not user_detail:
            # If we cannot fetch the detailed profile, we shouldn't attempt to show Follow actions.
            print_error("Could not fetch user profile details.")
            return "BACK" # Go back to user directory if details can't be fetched
        
        # Use tables for perfect alignment of keys and values
        info_grid = Table.grid(padding=(0, 2))
        info_grid.add_column(style="bold cyan")
        info_grid.add_column(style="white")
        
        info_grid.add_row("Username:", user_detail.user_name)
        info_grid.add_row("First Name:", user_detail.first_name or "N/A")
        info_grid.add_row("Last Name:", user_detail.last_name or "N/A")
        info_grid.add_row("Joined:", user_detail.created_at.strftime("%Y-%m-%d"))

        stats_grid = Table.grid(padding=(0, 2))
        stats_grid.add_column(style="bold magenta")
        stats_grid.add_column(style="yellow")
        
        stats_grid.add_row("Posts:", str(user_detail.post_count))
        stats_grid.add_row("Followers:", str(user_detail.followers_count))
        stats_grid.add_row("Following:", str(user_detail.following_count))

        # Construct the layout using a Group for better structure
        layout_group = Group(
            info_grid,
            "\n[bold cyan]Bio:[/bold cyan]",
            f"[italic white]{user_detail.bio or 'No biography provided.'}[/italic white]\n",
            stats_grid
        )
        
        console.print(
            Panel(
                layout_group, 
                title=f"[bold blue]User Profile: {user_detail.user_name}[/bold blue]", 
                border_style="blue",
                padding=(1, 2),
                expand=False
            )
        )
        
        # Check if the logged-in user is viewing their own profile
        is_own_profile = session.user and session.user.get("id") == user_detail.id
        choices = ["View Following","Back"]

        if not is_own_profile:
            if user_detail.is_following: # Use user_detail.is_following
                choices.insert(0, "Unfollow")
            else:
                choices.insert(0, "Follow")
        
            # Add the "View Following" option
            
                
        action = questionary.select("Actions:", choices=choices).ask()

        # Handle user cancelling the selection (Ctrl+C) or choosing Back
        if action is None or action == "Back": 
            return "BACK"

        # Handle menu actions
        if action == "Follow":
            if follow_user(user_detail.id): 
                print_success(f"You are now following {user_detail.user_name}!")
            else:
                print_error("Follow action failed.")
            # No return needed; loop will clear screen and fetch fresh data
            
        elif action == "Unfollow":
            if unfollow_user(user_detail.id): 
                print_success(f"You unfollowed {user_detail.user_name}.")
            else:
                print_error("Could not unfollow user.")
        
        elif action == "View Following":
            following_list = get_followed_users(user_detail.id) 
            followers_list = get_followers(user_detail.id)

            console.print("\n[bold magenta]Social Connections:[/bold magenta]")

            console.print("\n[cyan]Following:[/cyan]")
            if not following_list:
                console.print("  [dim]No following found.[/dim]")
            else:
                for u in following_list:
                    console.print(f"  - {u.user_name}")

            console.print("\n[cyan]Followers:[/cyan]")
            if not followers_list:
                console.print("  [dim]No followers found.[/dim]")
            else:
                for u in followers_list:
                    console.print(f"  - {u.user_name}")

            print("\n")
            pause() # Pause to allow user to read the list before loop clears screen