from console_app.state import session
from .global_feed import global_feed_screen
from .following_feed import following_feed_screen
from .create_post import create_post_screen
from .user_directory import user_directory_screen
from .utils import print_header, clear_screen
import questionary

def main_menu_screen():
    """Displays the main menu of the console app"""
    clear_screen()
    print_header ("Social Media App", "Main Menu")

    answer = questionary.select(
        message="",
        qmark = "",
        instruction=" ",
        choices=[
            "Global Feed",
            "Following Feed",
            "Create Post",
            "Member Dictionary",
            "Logout",
            "Exit"
        ]).ask()
    
    match answer:
        case "Global Feed":
            return global_feed_screen
        case "Following Feed":
            return following_feed_screen
        case "Create Post":
            return create_post_screen
        case "Member Dictionary":
            return user_directory_screen
        case "Logout":  
            session.logout()
            return "EXIT"
        case "Exit":
            return "EXIT"
        case _:
            return "HOME"