from .ui import (
    welcome_screen,
    login_screen,
    register_screen,
    main_menu_screen,
    user_details_screen,
    user_directory_screen,
    global_feed_screen,
    following_feed_screen,
    create_post_screen,
    end_app_screen
)
from .constants import UIScreen
from .state import session
from .client_api import get_my_user
from web_app.models import UserRead

# The main program, starting the main menu
if __name__ == "__main__":

    # Startup check, load token
    if session.load_token():
        try:
            # Try to fetch user data with the saved token
            user: UserRead | None = get_my_user()
            if user:
                next_screen = UIScreen.MAIN_MENU
            else:
                next_screen = UIScreen.WELCOME
        except:
            next_screen = UIScreen.WELCOME
    else:
        next_screen = UIScreen.WELCOME

    # Screen selection
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
            case UIScreen.USER_DIRECTORY:
                next_screen = user_directory_screen()
            case UIScreen.USER_DETAILS:
                next_screen = user_details_screen()
            case UIScreen.GLOBAL_FEED:
                next_screen = global_feed_screen()
            case UIScreen.FOLLOWING_FEED:
                next_screen = following_feed_screen()
            case UIScreen.CREATE_POST:
                next_screen = create_post_screen()
            case UIScreen.EXIT:
                end_app_screen()
                break
            case _:
                print_error("Unavailable screen selected.")
        