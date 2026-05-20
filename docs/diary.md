# DIARY
## Week 1
### Mon May 4th 2026
- Merged initial architecture (Daniel)
- Divided and assigned tasks (all)
- Agreed on first sprint in Jira (all)

### Tue May 5th
- Created pull request (Daniel)
  - server-side authentication
  - Extracted authentication and url parameters into .env file
- Created pull request (Steven)
- implemented posts including CRUD functionality and routing
- Created pull request (Dominik)
    - Configured IAM user/group permissions for SSM access
    - Prepared the EC2 instance by installing Git, Python, pip, venv and useful CLI Tools
    - Cloned the Github repository and configured Bash for SSM sessions.

### Wed May 6th
- Created pull request (Steven)
- improved readability of the code by:
    - changing comment language to english
    - moving models, routes closer together
    - adding comments, headlines
- worked on merging pull requests for server-side authentication and user post functionality (Daniel)
- worked on design of SQLModel, REST API, and first draft of UI dialog flow (Daniel)
- Configured the FastAPI application on the EC2 instance to run as a persistent background service using systemd(Dominik)
- Verified that the application remains reachable on port 8000 after closing the SSM session(Dominik)

### Thu May 7th
- Created pull request (Daniel)
   - client side authentication
   - client api migration from requests to httpx
   - Refactored the UI and styled it for unified user experience
- worked on follow N:N logic (Steven)
  - implemented models for Follow
  - implemented Relationship between User and Follow
- Created pull request (Dominik)
  - Added comment model, CRUD functions and API endpoint
  - Updated post details to include nested comments
  - Tested comment creation and retrieval locally

### Wed May 20th
- Presentation Preparation (Daniel)
