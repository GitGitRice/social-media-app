from console_app.constants import UIScreen
from console_app.ui.utils import print_header, print_step,clear_screen
import questionary

def welcome_screen() -> UIScreen :

    clear_screen()
    print_header("Welcome", "Social Media App")
    
    answer = questionary.select(
        "What would you like to do?",
        choices=["Register", "Login", "Exit"]
    ).ask()
        
    if answer == "Register":
        return UIScreen.REGISTER
    elif answer == "Login":
        return UIScreen.LOGIN
    else:
        return UIScreen.EXIT