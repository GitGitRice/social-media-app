from .utils import print_header, clear_screen, print_error, print_success
from console_app.constants import UIScreen
from web_app.models import UserCreate, UserRead
from console_app.client_api import add_user
import questionary

def validate_password(text):
    if len(text) < 3:
        return "Password is too short (min 3 characters)"
    if len(text) > 8:
        return "Password is too long (max 8 characters)"
    return True

def register_screen() -> UIScreen:
    clear_screen()
    print_header ("Social Media App", "Register")

    """Display add user form and collect answers"""
    answers = questionary.form(
        user_name = questionary.text(
            "User Name (Mandatory)", 
            validate=lambda text: True if len(text.strip()) > 0 else "User Name cannot be empty!"),
        email = questionary.text(
            "Email (Mandatory)",
            validate=lambda text: True if "@" in text else "Please enter a valid email address."),
        first_name = questionary.text("First Name"),
        last_name = questionary.text("Last Name"),
        password = questionary.password(
            "Password (3-8 characters)",
            validate=validate_password),
        bio = questionary.text ("Biography", multiline=True)
    ).ask()

    if not answers:
        # User pressed Ctrl+C and cancelled the form
        print_error("Registration cancelled.")
        return UIScreen.WELCOME
    
    # the form entries return "", if user just pressed enter, but UserCreate expects None, if no value was supplied. So, we translate empty strings "" to None
    clean_answers = {k: (v if v.strip() != "" else None) for k, v in answers.items()}

    # Create UserCreate object and add through api to server
    user = UserCreate(
        user_name=str(clean_answers.get("user_name")), 
        email=str(clean_answers.get("email")),
        first_name=clean_answers.get("first_name"), 
        last_name=clean_answers.get("last_name"),
        password=str(clean_answers.get("password")), 
        bio=clean_answers.get("bio"))
    
    # Add user via client api to server
    created_user: UserRead | None = add_user(user)
    if created_user:
        print_success(f"{created_user.user_name} successfully registered.")
        return UIScreen.MAIN_MENU
    else:
        print_error("Registration failed.")
        return UIScreen.WELCOME
