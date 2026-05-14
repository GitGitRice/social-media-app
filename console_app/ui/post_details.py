from .utils import print_error,clear_screen,print_header, print_success, Emoji
from .create_comment import create_comment_screen
from console_app.client_api import get_post, get_my_user, toggle_like
import questionary
from rich.console import Console
from rich.tree import Tree
from rich import print

console = Console()

def post_details_screen(selected_post_id):

    # clear screen and print header
    clear_screen()
    print_header("Social Media App", "Post Details")


    # retrieve post with provided id
    selected_post = get_post(selected_post_id)
    
    # return BACK, if error during retrieval
    if selected_post == None:
        print_error("Error retrieving Post.")
        return "BACK"
    
    # build post content node with likes and comments counts
    post_content_node = selected_post.content
    if selected_post.comments_count > 0:
        post_content_node = post_content_node + f"\n{Emoji.COMMENT}({selected_post.comments_count})"
    if selected_post.likes_count > 0:
        post_content_node = post_content_node + " "*3 + f"{Emoji.LIKE}({selected_post.likes_count})"

    # build tree view with post_content_node and comments as child
    tree = Tree(post_content_node)
    for comment in selected_post.comments:
        tree.add(comment.content)
    print (tree)
    print("")

    # like status of logged in user to post
    logged_in_user = get_my_user()
    if not logged_in_user or not logged_in_user.id:
        print_error("Error retrieving logged in user")
        return "BACK"
    likes_of_user = [like.user_id for like in selected_post.likes if like.user_id == logged_in_user.id]
    user_liked_post = len(likes_of_user) > 0

    # user selection menu
    choice= questionary.select(
        "",
        choices=["Create Comment", "Unlike" if user_liked_post else "Like", "Back", "Home"],
        qmark="",           # Removes the "?"
        instruction=""      # Removes the "(Use arrow keys)"
    ).ask()

    # interpret user selection
    if choice == "Create Comment":
        return lambda: create_comment_screen(selected_post_id)
    elif choice == "Like" or choice == "Unlike":
        toggle_like(selected_post_id)
        print_success ("Liked" if not user_liked_post else "Unliked" + " Post")
        return "BACK"
    elif choice == "Back":
        return "BACK"
    elif choice == "Home":
        return "HOME"
    else:
        print_error("Error in Menu Selection")