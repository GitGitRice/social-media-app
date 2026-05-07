from enum import Enum

class UIScreen(str, Enum):
    """
    Contains the list of UI Screens of the application.
    """
    WELCOME = "WELCOME"
    REGISTER = "REGISTER"
    LOGIN = "LOGIN"
    MAIN_MENU = "MAIN_MENU"
    EXIT = "EXIT"