```mermaid
graph TD
    %% Main Entry Points
    Welcome[Welcome Screen]
    
    Welcome -- "User selects 'Register'" --> Registration
    Welcome -- "User selects 'Login'" --> Login
    
    Registration[Registration]
    Login[Login]
    
    Registration -- "Successful registration" --> MainMenu
    Login -- "Successful login" --> MainMenu
    
    %% Main Menu Hub
    MainMenu[Main Menu]
    
    MainMenu -- "Logout" --> Welcome
    MainMenu -- "View my feed" --> MyFeed
    MainMenu -- "View global feed" --> GlobalFeed
    MainMenu -- "Create a post" --> CreatePost
    MainMenu -- "View my profile" --> MyProfile
    
    %% Feed Actions
    MyFeed[My Feed]
    GlobalFeed[Global Feed]
    
    MyFeed -- "View post details" --> PostDetails
    GlobalFeed -- "View post details" --> PostDetails
    
    %% Post Interactions
    PostDetails[Post Details]
    
    PostDetails -- "View likes" --> ViewLikes
    PostDetails -- "View comments" --> ViewComments
    PostDetails -- "View user profile" --> OtherUserProfile
    
    ViewLikes -- "Back to post" --> PostDetails
    ViewComments -- "Back to post" --> PostDetails
    OtherUserProfile -- "Back to previous screen" --> PostDetails
    
    %% Profile Actions
    CreatePost -- "Post created" --> MainMenu
    
    MyProfile -- "Edit profile" --> EditProfile
    EditProfile -- "Profile updated" --> MyProfile
```