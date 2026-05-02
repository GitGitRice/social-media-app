# Architecture - Social Media App
## Overview
This is the architecture of the team project Social Media App.
## Web App
### Technology
- FastAPI
- Pydantic
- SQLModel
- sqlite3
### Modules
- main
- auth
- models
- crud
- database
## Console App
### Technology
- requests
- imports Pydantic models from web_app
- rich
- questionary
### Modules
- client
- ui
- api
## Virtual Environment
venv with folder .venv is used to install packages and run both apps. They share the same .venv folder.