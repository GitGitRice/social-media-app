#!/bin/bash

# 1. Define variables
VENV_DIR=".venv"
REQ_FILE="requirements.txt"
APP_FILE="web_app/main.py"

echo "🚀 Starting server initialization..."

# 2. Check if .venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Virtual environment not found. Creating $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Virtual environment already exists."
fi

# 3. Activate the environment
# Works for macOS/Linux
source "$VENV_DIR/bin/activate"

# 4. Install/Update dependencies if requirements.txt exists
if [ -f "$REQ_FILE" ]; then
    echo "📥 Installing dependencies from $REQ_FILE..."
    pip install --upgrade pip
    pip install -r "$REQ_FILE"
else
    echo "⚠️  $REQ_FILE not found. Skipping installation."
fi

# 5. Start the FastAPI server
echo "🔥 Starting FastAPI development server..."
fastapi dev "$APP_FILE"