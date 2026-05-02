# Social Media App

## Team
- Steven
- Dominik
- Daniel

## Setup Development Environment

### Overview to venv
Using venv as Virtual environment to install required packages in this environment and keep the global Mac environment clean.

### Check Python version
python3 --version should be 3.1x

### Create Virtual Environment
python3 -m venv .venv

If you are going to use the ./start_server.sh, this is not required.

### Activate .venv
source .venv/bin/activate

You can check the python3 version again to confirm the interpreter from .venv is active.

If you are going to use the ./start_server.sh, this is not required.

### Install required packages into .venv
pip install sqlmodel
pip install "fastapi[standard]"
pip install requests

Alternatively, you can install pip install -r requirements.txt

### Start Server
./start_server.sh

Alternatively, you can run "fastapi dev web_app/main.py" after having activated the .venv environment.

### Start Console Client
Dont forget to activate .venv for this console
./start_client.sh

Alternatively, you can run "python3 -m console_app.client" after having activated the .venv environment.

### Deactivate .venv
deactivate