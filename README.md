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

### Activate .venv
source .venv/bin/activate

You can check the python3 version again to confirm the interpreter from .venv is active.

### Install required packages into .venv
pip install sqlmodel
pip install "fastapi[standard]"
pip install requests

### Start Server
Dont forget to activate .venv for this console
./start_server.sh

### Start Console Client
Dont forget to activate .venv for this console
./start_client.sh

### Deactivate .venv
deactivate