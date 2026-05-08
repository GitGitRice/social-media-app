from .utils import print_header, print_error, clear_screen
from console_app.constants import UIScreen
from console_app.client_api import login_user
import questionary

def login_screen() -> UIScreen:
    """Asks for username and password to login the user."""
    
    clear_screen()
    print_header ("Social Media App", "Login")
    
    # Display add user form and collect answers
    answers = questionary.form(
        user_name = questionary.text("User Name"),
        password = questionary.password("Password")

    ).ask()

    if not answers:
        # User pressed Ctrl+C and cancelled the form
        print_error("Login cancelled.")
        return UIScreen.WELCOME
    
    if login_user(user_name=answers["user_name"], password=answers["password"]):
        return UIScreen.MAIN_MENU
    else:
        print_error("Username or Password wrong.", with_pause=True)
        return UIScreen.WELCOME