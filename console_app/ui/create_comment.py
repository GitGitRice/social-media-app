from .utils import clear_screen, print_header, print_error, print_success
import questionary
from console_app.client_api import create_comment, get_post

from rich import print
from rich.panel import Panel
      
def create_comment_screen (selected_post_id: int):

    # clear screen and print header
    clear_screen()
    print_header("Social Media App", "Comment Post")

    # show post content
    selected_post = get_post(selected_post_id)
    if not selected_post:
        print_error("Post could not be retrieved")
        return "BACK"
    
    print(Panel(selected_post.content))

    # collect comment
    comment = questionary.text("", multiline=True).ask()
    if comment == None:
        return "BACK"
    
    # create comment on server
    if (create_comment(selected_post_id, comment)):
        print_success ("Comment created")
        return "BACK"
    else:
        print_error ("Error creating comment")
        return "BACK"
    