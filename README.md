# Social Media App

## Development Environment

### Overview to venv
Using venv as Virtual environment to install required packages in this environment and keep the global Mac environment clean.

### Create Virtual Environment .venv
Note: If you are going to use the ./start_server.sh, creating .venv manually is not required. It is done automatically by the script.

Manual Process:
Execute python3 -m venv .venv

### Activate .venv
Note: If you are going to use the ./start_server.sh, activating .venv manually is not required. It is done automatically by the script.

Manual Process:
Execute source .venv/bin/activate

You can use "which python" to confirm the interpreter from .venv is active.
With "python --version" you can confirm the python version.

### Install required packages into .venv

Note: If you are going to use the ./start_server.sh, installing the packages manually is not required. It is done automatically by the script.

Manual Process:
Either single installations of the packages.
- pip install sqlmodel
- pip install "fastapi[standard]"
- pip install requests
- pip install questionary
- pip install rich

Alternatively, you can install pip install -r requirements.txt which installs all missing packages.

### Start Server
./start_server.sh

Alternatively, you can run "fastapi dev web_app/main.py" after having activated the .venv environment and installed the dependencies.

### Start Console Client
Dont forget to activate .venv for this console
./start_client.sh

Alternatively, you can run "python3 -m console_app.client" after having activated the .venv environment and installed the dependencies.

### Deactivate .venv
deactivate