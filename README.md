# Social Media App

Welcome to the **Social Media App**! This project is designed as an introductory team project to learn the fundamentals of full-stack development, API design, and database management.

---

## Overview

This application consists of two main parts:
1.  **Backend API**: Built with **FastAPI**, it handles data storage, user authentication, and business logic.
2.  **Console Client**: A interactive CLI application built with **Questionary** and **Rich** that lets you interact with the social network right from your terminal.

---

## Core Features

- **User Management**: Register, Login, and manage your profile.
- **Social Interaction**: Follow other users, see their posts, and engage.
- **Content Creation**: Create posts, leave comments, and like what you see!
- **Notifications**: Stay updated with email notifications for new followers and interactions.

---

## The Tech Stack (Why we chose these)

- **Python 3.13+**: The core language. Clean, readable, and powerful.
- **FastAPI**: A modern, high-performance web framework for building APIs with Python. It's great because it automatically generates documentation!
- **SQLModel (SQLAlchemy + Pydantic)**: Makes working with databases feel like writing regular Python code.
- **SQLite**: A lightweight, file-based database—perfect for getting started without setting up a heavy server.
- **Rich & Questionary**: Used in the Console Client to make the terminal look beautiful and interactive.

---

## Getting Started

We've made it easy to get up and running! Follow these steps:

### 1. Environment Variables

This project uses environment variables for configuration. A `.env.example` file is provided to help you set up your environment.

**Step 1: Create your `.env` file**

Copy the `.env.example` file to a new file named `.env` in the root of your project:

```bash
cp .env.example .env
```

**Step 2: Configure your environment variables**

Open the newly created `.env` file and update the values as needed. For example, you might configure your `SERVER_URL` for the console app to connect to a remote server.

---

### 2. The Quick Start (Recommended)

The easiest way to start is using our helper scripts. They automatically handle setting up your virtual environment and installing everything you need.

**Step 1: Start the Server**
Open a terminal and run:
```bash
./start_server.sh
```
*Wait for the message saying the server is running (usually at http://127.0.0.1:8000).*

**Step 2: Start the Client**
Open a **new** terminal window and run:
```bash
./start_client.sh
```
*Now you can start interacting with the app!*

---

### 3. Manual Setup (For the Curious)

If you want to understand how things work under the hood:

1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    ```
    *Why? This keeps your project's dependencies isolated from the rest of your computer.*

2.  **Activate it**:
    ```bash
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    These are the dependencies, which are key to the project:
    ```bash
    pip install sqlmodel
    pip install "fastapi[standard]"
    pip install requests
    pip install questionary
    pip install rich
    pip install bcrypt
    pip install "python-jose[cryptography]"
    pip install python-dotenv

    ```

4.  **Run the Server manually**:
    ```bash
    fastapi dev web_app/main.py
    ```
5.  **Run the Client manually**:
    ```bash
    python3 -m console_app.client
    ```

---

## Project Structure

- `web_app/`: The heart of the backend. Contains models, database logic, and API endpoints.
- `console_app/`: The terminal-based user interface.
- `docs/`: Technical documentation ([Architecture](docs/architecture.md), [Project Plan](docs/project_plan.md)).

---

## Tips

- **Explore the API**: Once the server is running, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the interactive API documentation. You can test endpoints directly from your browser!
- **Check the Database**: The `database.db` file is a SQLite database. You can use tools like [DB Browser for SQLite](https://sqlitebrowser.org/) to see how your data is stored.
- **Read the Code**: Start with `web_app/main.py` and `console_app/client.py` to see how the two parts talk to each other.

Happy Coding, Licht und Frieden!
