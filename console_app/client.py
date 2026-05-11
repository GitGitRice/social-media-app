from .ui import welcome_screen, main_menu_screen


from .state import session
from .client_api import get_my_user
from web_app.models import UserRead

# The main program, starting the main menu
if __name__ == "__main__":

    # stack to hold ui screens
    ui_screen_stack = []

    # load token at application startup
    if session.load_token():
        try:
            # Try to fetch user data with the saved token
            user: UserRead | None = get_my_user()
            if user:
                # We create a local alias to ensure that the lambda is called with not-None active_user
                active_user: UserRead = user
                ui_screen_stack = [main_menu_screen]
            else:
                ui_screen_stack = [welcome_screen]
        except:
            ui_screen_stack = [welcome_screen]
    else:
        ui_screen_stack = [welcome_screen]

    # Screen selection
    while True:

        # take the screen from the stack (the last which was pushed to the stack)
        current_screen = ui_screen_stack[-1]

        # call this last screen
        result = current_screen()
        if result == "BACK":
            # remove the last screen from stack
            ui_screen_stack.pop()
        elif result == "EXIT":
            # exit the app
            break
        elif result == "HOME":
            # reset the stack to the main menu, deleting all intermediate screens
            ui_screen_stack = [main_menu_screen]
        elif result == "LOGOUT":
            ui_screen_stack = [welcome_screen]
        elif isinstance (result, tuple) and result[0] == "AUTH_SUCCESS":
            # reset the stack to the returned screen only. This is done after login to have only the home screen on the stack and BACK wouldnt work
            ui_screen_stack = [result[1]]
        elif callable(result):
            # a new screen was returned. Add it as last screen to the stack
            ui_screen_stack.append(result)
        else:
            print ("Error in menu selection")
            break