from console_app.ui.utils import print_header, print_step,clear_screen, print_error
from .login import login_screen
from .register import register_screen
import questionary

def welcome_screen():

    clear_screen()
    print_header("Social Media App", "Welcome")
    
    answer = questionary.select(
        "What would you like to do?",
        choices=["Register", "Login", "Exit"]
    ).ask()
        
    if answer == "Register":
        return register_screen
    elif answer == "Login":
        return login_screen
    elif answer == "Exit":
        return "EXIT"
    else:
        print_error ("Error in Menu Selection. Exiting App.")
        return "EXIT"
        