import questionary
from web_app.models import PostRead
from .post_details import post_details_screen
from .utils import Emoji

def build_feed_screen_selector (posts: list [PostRead]):
    """Builds the selection menu for the feed screens and interprets the user selection"""
    
    # build choice menu of posts, plus HOME
    choices=[build_post_menu_item(post) for post in posts]
    choices.append("Home")
    
    # ask for user choice
    choice = questionary.select(
        "",
        choices=choices
    ).ask()

    # interpret user choice
    if choice == "Home":
        return "HOME"
    else:
       # the first line of the post in the choice menu is the post id
       selected_post_id = int(choice.split("\n")[0])
       return lambda: post_details_screen(selected_post_id)

def build_post_menu_item (post: PostRead):
    """Builds a menu item for a post to be inserted into questionary.select"""

    # rebuild the multi-line text, aligning with the menu layout
    post_lines = post.content.split("\n")
    post_menu_item = f"{post.id}"
    for post_line in post_lines:
        post_menu_item = post_menu_item + "\n" + " "*3 + post_line

    # add comments count and likes count as additional line
    post_menu_item = post_menu_item + "\n" + " "*6
    if post.comments_count > 0:
        post_menu_item = post_menu_item + f"{Emoji.COMMENT}({post.comments_count})" + " "*3
    if post.likes_count > 0:
        post_menu_item = post_menu_item + f"{Emoji.LIKE}({post.likes_count})"

    return post_menu_item