import questionary
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

from web_app.models import UserCreate, UserRead
from console_app.client_api import add_user, get_users

console = Console()

def add_user_ui() -> None:

    # Display add user form and collect answers
    answers = questionary.form(
        user_name = questionary.text(
            "User Name (Mandatory)", 
            validate=lambda text: True if len(text.strip()) > 0 else "User Name cannot be empty!"),
        first_name = questionary.text("First Name"),
        last_name = questionary.text("Last Name"),
        bio = questionary.text ("Biography", multiline=True)
    ).ask()

    if not answers:
        # User pressed Ctrl+C and cancelled the form
        print("Adding User was cancelled.")
        return
    
    # form entries return "", if user just presses enter, but UserCreate expects None, if no value was specified. So, we translate "" to None
    clean_answers = {k: (v if v.strip() != "" else None) for k, v in answers.items()}

    # Create UserCreate object and add through api to server
    user = UserCreate(
        user_name=str(clean_answers.get("user_name")), 
        first_name=clean_answers.get("first_name"), 
        last_name=clean_answers.get("last_name"), 
        bio=clean_answers.get("bio"))
    add_user(user)

def show_user_ui(user: UserRead) -> None:
    """Displays detailed information about a single user."""
    from rich.panel import Panel
    
    detail_content = (
        f"[bold]Username:[/bold] {user.user_name}\n"
        f"[bold]First Name:[/bold] {user.first_name or 'N/A'}\n"
        f"[bold]Last Name:[/bold] {user.last_name or 'N/A'}\n"
        f"[bold]Bio:[/bold] {user.bio or 'No biography provided.'}\n"
        f"[bold]Created:[/bold] {user.created_at}"
    )
    
    console.print(Panel(detail_content, title=f"User Profile: {user.user_name}", expand=False))
    
    questionary.press_any_key_to_continue().ask()

def get_users_ui() -> None:
    
    users = get_users()
    if not users:
        console.print("\n[yellow]No Users found in the database.[/yellow]\n")
        questionary.press_any_key_to_continue().ask()
        return

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
        return
    
    # Find the specific user object that matches the selection
    selected_user = next(u for u in users if u.user_name == selection)
    show_user_ui(selected_user)

def main_menu_ui() -> None:
    
    while True:
        answer = questionary.select(
            message="Main Menu",
            qmark = "",
            instruction=" ",
            choices=[
                "Add User",
                "Display Users",
                "Exit"
            ]).ask()
        match answer:
            case "Add User":
                add_user_ui()
            case "Display Users":
                get_users_ui()
            case "Exit":
                break
            case _:
                # can only trigger, if programmer used the wrong strings in case statement
                print("Invalid Selection") 
                continue
