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
    MainMenu -- "Personalized Feed" --> PersonalizedFeed
    MainMenu -- "Create Post" --> CreatePost
    MainMenu -- "Member Dictionary" --> UserDirectory
    MainMenu -- "Logout" --> Welcome
    MainMenu -- "Exit" --> ExitApp
    
    %% Feed Actions
    GlobalFeed[Global Feed]
    GlobalFeed -- "Press any key" --> MainMenu
    GlobalFeed -- "Select Post" --> PostDetails
    GlobalFeed -- "Back" --> MainMenu

    PersonalizedFeed[Personalized Feed]
    PersonalizedFeed -- "Select Post" --> PostDetails
    PersonalizedFeed -- "Back" --> MainMenu
    
    %% User Actions
    UserDirectory[User Directory]
    UserDirectory -- "Select User" --> UserDetails
    UserDirectory -- "Back" --> MainMenu

    
    UserDetails[User Details]
    UserDetails -- "Back" --> UserDirectory
    UserDetails -- "Home" --> MainMenu

    %% Post Actions
    CreatePost[Create Post]
    CreatePost -- "Post submitted / failed" --> MainMenu
    
    PostDetails[Post Details]
    PostDetails -- "Add Comment" --> CreateComment
    %% Simplified: "Back" returns to the previous screen on the stack (e.g., a feed)
    PostDetails -- "Back" --> MainMenu 

    CreateComment[Create Comment]
    CreateComment -- "Submitted / Cancelled" --> PostDetails


    ExitApp[Exit]
```

## Information Items Displayed per Dialog

- **Welcome Screen**: Application header, prompt to select an action ("Register", "Login", "Exit").
- **Registration**: Form fields to collect User Name (mandatory), First Name, Last Name, Password (3-8 characters), and Biography. Displays registration success or cancellation/failure messages.
- **Login**: Form fields to collect User Name and Password. Displays login success or cancellation/failure messages.
- **Main Menu**: Application header, menu options ("Global Feed", "Personalized Feed", "Create Post", "Member Dictionary", "Logout", "Exit").
- **Global Feed**: A selectable list of all posts in the system. Each post displays its ID, Content, and counts for comments and likes. Shows an empty feed message if no posts exist. Prompts to select a post or return Home.
- **Personalized Feed**: A selectable list of posts from users the current user follows. Each post displays its ID, Content, and counts for comments and likes. Shows an empty feed message if no posts exist. Prompts to select a post or return Home.
- **User Directory**: A tabular list of all users displaying ID, Username, and Created At date. Prompts to select a specific user or return to the main menu.
- **User Details**: Detailed profile of the selected user, including Username, First Name, Last Name, Bio, and Created At timestamp. Prompts to go back.
- **User Details**: Detailed profile of the selected user, including Username, First Name, Last Name, Bio, and Created At timestamp. Provides options to **Follow/Unfollow** the user and to go back.
- **Create Post**: Prompt to enter post content ("Was möchtest du teilen?"). Displays post creation success or error messages.
- **Post Details**: Displays the full content of a single post, its author, and a list of all associated comments. Provides options to **Like/Unlike** the post, "Add Comment", or go "Back".
- **Create Comment**: Prompt to enter comment content. Displays comment creation success or cancellation messages.
- **Exit**: Terminates the application.
