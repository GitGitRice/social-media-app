# UI Dialog Flow

```mermaid
flowchart LR
    %% Main Entry Points
    Startup[App Startup]
    Welcome[Welcome Screen]
    
    Startup -- "Valid Token" --> MainMenu
    Startup -- "No Token / Invalid" --> Welcome

    Welcome -- "Register" --> Registration
    Welcome -- "Login" --> Login
    Welcome -- "Exit" --> ExitApp
    
    Registration[Registration]
    Login[Login]
    
    Registration -- "Successful registration" --> MainMenu
    Registration -- "Cancelled / Failed" --> Welcome
    
    Login -- "Successful login" --> MainMenu
    Login -- "Cancelled / Failed" --> Welcome
    
    %% Main Menu Hub
    MainMenu[Main Menu]
    
    MainMenu -- "Global Feed" --> GlobalFeed
    MainMenu -- "Create Post" --> CreatePost
    MainMenu -- "Member Dictionary" --> UserDirectory
    MainMenu -- "Logout" --> Welcome
    MainMenu -- "Exit" --> ExitApp
    
    %% Feed Actions
    GlobalFeed[Global Feed]
    GlobalFeed -- "Press any key" --> MainMenu
    
    %% User Actions
    UserDirectory[User Directory]
    UserDirectory -- "Select User" --> UserDetails
    UserDirectory -- "Back" --> MainMenu

    UserDetails[User Details]
    UserDetails -- "Back" --> UserDirectory

    %% Post Actions
    CreatePost[Create Post]
    CreatePost -- "Post submitted / failed" --> MainMenu

    ExitApp[Exit]
```

## Information Items Displayed per Dialog

- **Welcome Screen**: Application header, prompt to select an action ("Register", "Login", "Exit").
- **Registration**: Form fields to collect User Name (mandatory), First Name, Last Name, Password (3-8 characters), and Biography. Displays registration success or cancellation/failure messages.
- **Login**: Form fields to collect User Name and Password. Displays login success or cancellation/failure messages.
- **Main Menu**: Application header, menu options ("Global Feed", "Create Post", "Member Dictionary", "Logout", "Exit").
- **Global Feed**: A list of posts in the system. Each post displays its Content, Post ID, and Author ID. Shows an empty feed message if no posts exist. Prompts to press any key to return.
- **User Directory**: A tabular list of all users displaying ID, Username, and Created At date. Prompts to select a specific user or return to the main menu.
- **User Details**: Detailed profile of the selected user, including Username, First Name, Last Name, Bio, and Created At timestamp. Prompts to go back.
- **Create Post**: Prompt to enter post content ("Was möchtest du teilen?"). Displays post creation success or error messages.
- **Exit**: Terminates the application.
