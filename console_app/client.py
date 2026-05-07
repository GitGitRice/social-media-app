from .ui import (
    welcome_screen,
    login_screen,
    register_screen,
    main_menu_screen,
    end_app_screen
)

from .constants import UIScreen

from enum import Enum


# The main program, starting the main menu
if __name__ == "__main__":

    print ("Starting client.")
    next_screen = UIScreen.WELCOME
    while True:
        match next_screen:
            case UIScreen.WELCOME:
                next_screen = welcome_screen()
            case UIScreen.REGISTER:
                next_screen = register_screen()
            case UIScreen.LOGIN:
                next_screen = login_screen()
            case UIScreen.MAIN_MENU:
                next_screen = main_menu_screen()
            case UIScreen.EXIT:
                end_app_screen()
                break
            case _:
                print_error("Unavailable screen selected.")
        