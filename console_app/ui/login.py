from .utils import print_header, pause, clear_screen
from console_app.constants import UIScreen

def login_screen() -> UIScreen:
    clear_screen()
    print_header ("Login", "Social Media App")
    pause ("Login Screen")
    return UIScreen.WELCOME