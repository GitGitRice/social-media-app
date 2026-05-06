import os
import platform
from rich.console import Console
import questionary

console = Console()

def clear_screen() ->None:
    """Clears the screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def pause(message: str="Press any key to return to menu...") -> None:
    """Shows the provided message to the user, who can continue by pressing any key"""
    questionary.press_any_key_to_continue(
        message=message
    ).ask()

def print_error(message: str = "ERROR") -> None:
    """prints the provided message in red as error message"""
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_success(message: str = "SUCCESS") -> None:
    """prints the provided message in green as success message"""
    console.print(f"[bold green]Error:[/bold green] {message}")