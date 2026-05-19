from .utils import print_header, print_error, clear_screen
from console_app.client_api import login_user, get_my_user


import questionary

def login_screen():
    """Asks for username and password to login the user."""
    
    clear_screen()
    # Import main_menu_screen locally to break the circular dependency
    from .main_menu import main_menu_screen

    print_header ("Social Media App", "Login")
    
    # Display add user form and collect answers
    answers = questionary.form(
        user_name = questionary.text("User Name"),
        password = questionary.password("Password")

    ).ask()

    if not answers:
        # User pressed Ctrl+C and cancelled the form
        print_error("Login cancelled.")
        return "BACK"
    
    if login_user(user_name=answers["user_name"], password=answers["password"]):
        logged_in_user = get_my_user()
        if not logged_in_user:
            return "BACK"
        
        return ("AUTH_SUCCESS", main_menu_screen)
    else:
        print_error("Username or Password wrong.", with_pause=True)
        return "BACK"