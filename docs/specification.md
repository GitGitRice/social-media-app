# Specification - Social Media App
## Overview
This is the specification of the team project Social Media App. The functionality is ordered by approximate order of implementation (to be reviewed).
## Functionality
### Register User
### Login
### Logout
- logout could be automatic when closing the console app. This would require a login after each console app start.
- Alternatively, login data (not the password!) can be stored on disc in console app. This means that after console app start, user is logged in 
### View Own User Profile
### View List of Users
### View Other's User Profile
### Create Post
### View Inbox
### View Posts
### Like/Unlike Post
### Create Comment on Post
### Follow User
### Email Notifications
- New Follower
- New Post from Follower
- ...
### Unfollow User
### Like/Unlike Comment
### Edit Own User Profile
### Delete Post
### Delete Comment
### Unregister User
## Non-functional Requirements
### Deploy Server on Amazon EC2
- should integrate with GitHub to obtain the latest code
- Proposal: Two EC2 instances, with access for each team member
### Deployable Client on S3
- may be too much effort, as ideally we would create Windows .exe and Mac .app just for the demo.
