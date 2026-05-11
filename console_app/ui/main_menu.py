from console_app.constants import UIScreen
from .utils import print_header, clear_screen
from console_app.state import session
import questionary


def main_menu_screen() -> UIScreen:
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
            return UIScreen.GLOBAL_FEED
        case "Following Feed":
            return UIScreen.FOLLOWING_FEED
        case "Create Post":
            return UIScreen.CREATE_POST
        case "Member Dictionary":
            return UIScreen.USER_DIRECTORY
        case "Logout":  
            session.logout()
            return UIScreen.WELCOME
        case "Exit":
            return UIScreen.EXIT
        case _:
            return UIScreen.MAIN_MENU