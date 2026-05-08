from enum import Enum

class UIScreen(str, Enum):
    """
    Contains the list of UI Screens of the application.
    """
    WELCOME = "WELCOME"
    REGISTER = "REGISTER"
    LOGIN = "LOGIN"
    MAIN_MENU = "MAIN_MENU"
    USER_DIRECTORY = "USER_DIRECTORY"
    USER_DETAILS = "USER_DETAILS"
    GLOBAL_FEED = "GLOBAL_FEED"
    CREATE_POST = "CREATE_POST"
    EXIT = "EXIT"