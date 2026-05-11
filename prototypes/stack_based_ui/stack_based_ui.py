import questionary
from rich.console import Console

# Simulation of api response
PLANET_DATA = {
    "Earth": {
        "description": "Our home planet, the only one known to harbor life.",
        "moons": [
            {"name": "The Moon", "description": "Earth's only natural satellite."}
        ]
    },
    "Mars": {
        "description": "The Red Planet, home to Olympus Mons.",
        "moons": [
            {"name": "Phobos", "description": "The larger, inner moon of Mars."},
            {"name": "Deimos", "description": "The smaller, outer moon of Mars."}
        ]
    },
    "Jupiter": {
        "description": "The largest planet in our solar system, a gas giant.",
        "moons": [
            {"name": "Io", "description": "The most volcanically active body in the solar system."},
            {"name": "Europa", "description": "An icy moon with a suspected subsurface ocean."},
            {"name": "Ganymede", "description": "The largest moon in the solar system."},
            {"name": "Callisto", "description": "The most heavily cratered object in the system."}
        ]
    },
    "Saturn": {
        "description": "Famous for its extensive and bright ring system.",
        "moons": [
            {"name": "Titan", "description": "The only moon with a dense atmosphere."},
            {"name": "Enceladus", "description": "An icy moon with active water geysers."},
            {"name": "Mimas", "description": "Famous for its giant crater, looking like the Death Star."}
        ]
    }
}

def get_moon_description (planet_name, moon_name):
    moons = PLANET_DATA[planet_name]["moons"]
    return [moon["description"] for moon in moons if moon["name"] == moon_name][0]


# stack for ui screen functions
ui_stack = []

# simulating if user has access token stored on disc
access_token_available: bool = True

# Rich console
console = Console()

def welcome_screen():
    console.clear()
    # print welcome message
    console.print("Welcome")

    # build selection menu
    choice = questionary.select(
        "Select Option",
        choices = ["login", "register", "exit"]
    ).ask()

    if choice == "login":
        return lambda: login_screen()
    elif choice == "register":
        return lambda: register_screen()
    else:
        return "EXIT"
    
def login_screen():
    console.clear()
    console.print ("Login")
    user: str = questionary.text("Username:").ask()

    # simulate successfull vs. unsuccessfull login
    choice = questionary.select(
        "Simulate Login result",
        choices=["successfull", "unsuccessfull", "Back to Welcome"]
    ).ask()

    if choice == "successfull":
        return ("AUTH_SUCCESS", lambda: main_menu_screen(user))
    elif choice == "unsuccessfull":
        # registration unsuccessful or Back selected
        questionary.press_any_key_to_continue(
            message="Login unsuccessfull"
        ).ask()
        return "BACK"
    else:
        return "BACK"

def register_screen():
    console.clear()
    console.print ("Register Screen")

    # simulate registration
    console.print("user registers")

    choice = questionary.select(
        "Simulate Registration Result",
        choices=[
            "Registration successful", 
            "Registration not successfull", 
            "Back to Welcome"
        ]
    ).ask()

    if choice == "Registration successful":
        questionary.press_any_key_to_continue(
            message="Registration successfull"
        ).ask()
        return "BACK"
    elif choice == "Registration not successfull":
        questionary.press_any_key_to_continue(
            message="Registration not successfull"
        ).ask()
        return "BACK"
    else:
        return "BACK"

def main_menu_screen(user_name: str):
    console.clear()
    console.print ("Main Menu")
    # print user data
    console.print (f"user: {user_name}")

    # build selection menu
    choices = list(PLANET_DATA.keys())
    choices.append("Exit")
    choice = questionary.select(
        "Select Planet:",
        choices= choices
    ).ask()

    # interpret user selection
    if choice == "Exit":
        return "EXIT"
    else:
        return lambda: planet_screen(user_name, choice)

def planet_screen(user_name: str, planet_name: str):
    console.clear()
    console.print ("Planet Screen")
    # print user and planet data
    console.print (f"user: {user_name}")
    console.print (f"planet name: {planet_name}")
    console.print (f"planet details:", PLANET_DATA[planet_name]["description"])

    # build selection menu
    choices = [moon["name"] for moon in PLANET_DATA[planet_name]["moons"]]
    choices.append ("Back")
    choices.append ("Home")
    choice = questionary.select(
        "Select Moon:",
        choices = choices
    ).ask()

    # interpret user selection
    if choice == "Back":
        return "BACK"
    elif choice == "Home":
        return "HOME"
    else:
        return lambda : moon_screen (user_name=user_name, planet_name=planet_name, moon_name=choice)

def moon_screen (user_name, planet_name, moon_name):
    console.clear()
    console.print("Moon Screen")
    # print moon data
    console.print (f"user name: {user_name}")
    console.print (f"planet: {planet_name}")
    console.print (f"moon name: {moon_name}")
    console.print (f"moon details: {get_moon_description (planet_name, moon_name)}")

    # build selection menu
    choice = questionary.select ("", choices=["Back", "Home"]).ask()

    # interpret user selection
    if choice == "Back":
        return "BACK"
    elif choice == "Home":
        return "HOME"

if __name__ == "__main__":

    if access_token_available:
        ui_stack.append(lambda: main_menu_screen("user name from file"))
    else:
        ui_stack.append(welcome_screen)

    while True:
        # take the last screen from the stack
        current_screen = ui_stack[-1]

        # call this last screen
        result = current_screen()
        if result == "BACK":
            # remove the last screen from stack
            ui_stack.pop()
        elif result == "EXIT":
            # exit the app
            break
        elif result == "HOME":
            # reset the stack to the first item only, meaning delete all intermediate screens
            ui_stack = [ui_stack[0]]
        elif isinstance (result, tuple) and result[0] == "AUTH_SUCCESS":
            # reset the stack to the returned screen only. This is done after registration and login to have only the next screen (home screen) on the stack
            ui_stack = [result[1]]
        elif callable(result):
            # a new screen was returned. Add it as last screen to the stack
            ui_stack.append(result)
        else:
            print ("Error in menu selection")
            break