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

def print_error(message: str, with_pause: bool = True) -> None:
    """Prints a red error message. Optionally waits for user acknowledgement."""
    console.print(f"\n[bold red]Error:[/bold red] {message}")
    if with_pause:
        pause("Press any key to try again...")

def print_success(message: str, with_pause: bool = True) -> None:
    """Prints a green success message. Optionally waits for user acknowledgement."""
    console.print(f"\n[bold green]Success:[/bold green] {message}")
    if with_pause:
        pause() # Uses the default "Press any key to return to menu..."

def print_step(message: str) -> None:
    """Instructional step - usually doesn't need a pause."""
    console.print(f"[bold blue]❯[/bold blue] [white]{message}[/white]")