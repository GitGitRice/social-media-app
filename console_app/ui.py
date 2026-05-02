from web_app.models import UserCreate
from console_app.api import add_user, get_users

def add_user_ui() -> None:
    user_name = input ("user name: ")

    user = UserCreate(user_name=user_name)
    add_user(user)

def get_users_ui() -> None:
    users = get_users()
    print ("User List:")
    print ("----------")

    if len(users) == 0:
        print ("\nNo Users\n")
        return
    
    for user in users:
        print ("user name:", user.user_name)
        print ("created:", user.created_at)
        print ("-------------------------------------")

def main_menu_ui() -> None:
    while True:
        print ("Main Menu:")
        print ("1. Add User")
        print ("2. Display Users")
        print ("3. Exit")
        selection = input ("Select Option: ")
        match selection:
            case "1":
                add_user_ui()
            case "2":
                get_users_ui()
            case "3":
                break
