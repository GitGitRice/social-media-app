from .utils import clear_screen, print_header, print_error, print_success
import questionary
from console_app.client_api import create_comment

def create_comment_screen (selected_post_id: int):

    # clear screen and print header
    clear_screen()
    print_header("Social Media App", "Comment Post")

    # collect comment
    comment = questionary.text("", multiline=True).ask()

    # create comment on server
    if (create_comment(selected_post_id, comment)):
        print_success ("Comment created")
    else:
        print_error ("Error creating comment")

    # user selection menu
    choice= questionary.select(
        "",
        choices=["Back", "Home"],
        qmark="",           # Removes the "?"
        instruction=""      # Removes the "(Use arrow keys)"
    ).ask()

    # interpret user selection
    if choice == "Back":
        return "BACK"
    elif choice == "Home":
        return "HOME"
    else:
        print_error("Invalid choice")
        return "BACK"