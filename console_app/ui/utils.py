import os
import platform
from rich.console import Console
from rich.rule import Rule
from rich.panel import Panel
import questionary

console = Console()

def clear_screen() ->None:
    """Clears the screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_header(title: str, subtitle: str | None = "Social Media App") -> None:
    """
    Prints a consistent top-of-screen header.
    
    If None is provided for subtitle, no subtitle will be printed.
    """
    console.print(Rule(style="bold blue"))
    console.print(
        Panel(
            f"[bold cyan]{title}[/bold cyan]" + (f"\n[italic]{subtitle}[/italic]" if subtitle else ""),
            expand=True,
            border_style="blue",
            padding=(1, 2)
        )
    )

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

def print_step(message: str) -> None:
    """prints a message for the next step for the user"""
    console.print(f"[bold blue]❯[/bold blue] [white]{message}[/white]")