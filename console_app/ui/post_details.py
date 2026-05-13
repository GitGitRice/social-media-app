from rich.console import Console
# from console_app.client_api import get_post
import questionary

console = Console()

def post_details_screen(selected_post_id):
    console.print("Selected_post_id:", selected_post_id)
    choice= questionary.select(
        "",
        choices=["Back", "Home"]
    ).ask()

    if choice == "Back":
        return "BACK"
    elif choice == "Home":
        return "HOME"