import questionary
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

from web_app.models import UserCreate, UserRead, PostCreate
from console_app.client_api import add_user, get_users, add_post, get_posts, get_user_posts, remove_post

console = Console()

def validate_password(text):
    if len(text) < 3:
        return "Password is too short (min 3 characters)"
    if len(text) > 8:
        return "Password is too long (max 8 characters)"
    return True

def add_user_ui() -> None:
    """Display add user form and collect answers"""
    answers = questionary.form(
        user_name = questionary.text(
            "User Name (Mandatory)", 
            validate=lambda text: True if len(text.strip()) > 0 else "User Name cannot be empty!"),
        email = questionary.text(
            "Email (Mandatory)",
            validate=lambda text: True if "@" in text else "Please enter a valid email address."),
        first_name = questionary.text("First Name"),
        last_name = questionary.text("Last Name"),
        password = questionary.password(
            "Password (3-8 characters)",
            validate=validate_password),
        bio = questionary.text ("Biography", multiline=True)
    ).ask()

    if not answers:
        # User pressed Ctrl+C and cancelled the form
        print("Adding User was cancelled.")
        return
    
    # the form entries return "", if user just pressed enter, but UserCreate expects None, if no value was supplied. So, we translate empty strings "" to None
    clean_answers = {k: (v if v.strip() != "" else None) for k, v in answers.items()}

    # Create UserCreate object and add through api to server
    user = UserCreate(
        user_name=str(clean_answers.get("user_name")), 
        email=str(clean_answers.get("email")),
        first_name=clean_answers.get("first_name"), 
        last_name=clean_answers.get("last_name"),
        password=str(clean_answers.get("password")), 
        bio=clean_answers.get("bio"))
    
    # Add user via client api to server
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
    
    action = questionary.select(
            "Aktionen:",
            choices=["Posts ansehen", "Etwas posten", "Post löschen", "Zurück"]
        ).ask()

    if action == "Posts ansehen":
        user_posts = get_user_posts(user.id)
        for p in user_posts:
            console.print(f"- {p.content} ([dim]{p.created_at.strftime('%H:%M')}[/dim])")
        questionary.press_any_key_to_continue().ask()
    elif action == "Etwas posten":
        add_post_ui(user.id)
    elif action == "Post löschen":
        delete_post_ui()
        

def get_users_ui() -> None:
    """Shows list of all users and provides selection to user details"""
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
    """Displays the main menu of the console app"""
    while True:
        answer = questionary.select(
            message="Main Menu",
            qmark = "",
            instruction=" ",
            choices=[
                "Add User",
                "Display Users",
                "Globaler Feed",
                "Post löschen",
                "Exit"
            ]).ask()
        match answer:
            case "Add User":
                add_user_ui()
            case "Display Users":
                get_users_ui()
            case "Globaler Feed":
                show_feed_ui()
            case "Post löschen":  
                delete_post_ui()
            case "Exit":
                break
            case _:
                # can only trigger, if programmer used the wrong strings in case statement
                print("Invalid Selection") 
                continue


def show_feed_ui() -> None:
    """
    Shows newest posts of all users.
    """
    posts = get_posts()
    if not posts:
        console.print("[yellow]Der Feed ist noch leer.[/yellow]")
    else:
        for post in posts:
            console.print(Panel(post.content, title=f"Post ID: {post.id} (User {post.author_id})"))
    
    questionary.press_any_key_to_continue().ask()


def add_post_ui(user_id: int) -> None:
    """
    Enables currently logged in user to post posts.
    """
    content = questionary.text("Was möchtest du teilen?").ask()
    if content:
        post_data = PostCreate(content=content)
        if add_post(post_data):
            console.print("[green]Post erfolgreich veröffentlicht![/green]")
        else:
            console.print("[red]Fehler beim Posten.[/red]")


def delete_post_ui() -> None:
    """
    Asks for a post ID and deletes that post.
    """
    post_id = questionary.text("ID des zu löschenden Posts:").ask()
    if post_id and post_id.isdigit():
        confirm = questionary.confirm(f"Post {post_id} wirklich löschen?").ask()
        if confirm:
            if remove_post(int(post_id)):
                console.print("[green]Post wurde gelöscht.[/green]")
            else:
                console.print("[red]Fehler: Post konnte nicht gelöscht werden.[/red]")
    else:
        console.print("[yellow]Ungültige ID eingegeben.[/yellow]")
