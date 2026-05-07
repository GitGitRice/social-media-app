from console_app.constants import UIScreen
from .utils import print_header, pause, clear_screen

def main_menu_screen() -> UIScreen:
    """Displays the main menu of the console app"""
    clear_screen()
    print_header ("Main Menu", "Social Media App")
    pause ("Main Menu")
    return UIScreen.WELCOME
    # while True:
    #     answer = questionary.select(
    #         message="Main Menu",
    #         qmark = "",
    #         instruction=" ",
    #         choices=[
    #             "Add User",
    #             "Display Users",
    #             "Globaler Feed",
    #             "Post löschen",
    #             "Exit"
    #         ]).ask()
    #     match answer:
    #         case "Add User":
    #             add_user_ui()
    #         case "Display Users":
    #             get_users_ui()
    #         case "Globaler Feed":
    #             show_feed_ui()
    #         case "Post löschen":  
    #             delete_post_ui()
    #         case "Exit":
    #             break
    #         case _:
    #             # can only trigger, if programmer used the wrong strings in case statement
    #             print("Invalid Selection") 
    #             continue