from .utils import print_header, pause, clear_screen
from console_app.constants import UIScreen

def register_screen() -> UIScreen:
    clear_screen()
    print_header ("Register as User", "Social Media App")
    pause ("Register Screen")
    return UIScreen.WELCOME