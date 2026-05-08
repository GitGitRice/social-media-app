# Deployment Guide

This guide describes how to deploy and run the Social Media App backend on the EC2 server.

## Environment Variables

The app uses a `.env` file for configuration. Create it from the example file:

```bash
cp .env.example .env
```

Required values:

```env
DATABASE_URL=sqlite:///./database.db
SERVER_URL=http://<EC2_PUBLIC_IP>:8000
```

`DATABASE_URL` is used by the backend to access the database. For the current setup, SQLite stores the database file as `database.db` inside the project directory.

`SERVER_URL` is used by the local console client to connect to the API running on the EC2 instance. Use the public EC2 IP and port `8000`. Do not add `/docs` to the URL.

## Server Setup

Connect to the EC2 instance through AWS Systems Manager Session Manager and go to the project directory:

```bash
cd /opt/social-media-app
```

Pull the latest version from GitHub:

```bash
git pull origin main
```

Create and activate the Python virtual environment if needed:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure the project directory is writable by the SSM user. This is required because SQLite needs to create or update `database.db`:

```bash
sudo chown -R ssm-user:ssm-user /opt/social-media-app
```

## Running the App Manually

The FastAPI app can be started manually with:

```bash
python -m uvicorn web_app.main:app --host 0.0.0.0 --port 8000
```

The `--host 0.0.0.0` option is required so the app can accept requests from outside the EC2 instance.

After starting the server, test it in the browser:

```text
http://<EC2_PUBLIC_IP>:8000/docs
```

## Security Group

The EC2 security group must allow inbound traffic on port `8000` for the API to be reachable from the local client or browser.

SSH access on port `22` is not required because server access is handled through AWS Systems Manager Session Manager.

## systemd Service

To keep the app running after closing the SSM session, the app is configured as a `systemd` service.

Service file:

```bash
/etc/systemd/system/social-media-app.service
```

Example service configuration:

```ini
[Unit]
Description=Social Media FastAPI App
After=network.target

[Service]
User=ssm-user
Group=ssm-user
WorkingDirectory=/opt/social-media-app
EnvironmentFile=/opt/social-media-app/.env
ExecStart=/opt/social-media-app/.venv/bin/python -m uvicorn web_app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Reload systemd and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start social-media-app
```

Enable automatic startup after reboot:

```bash
sudo systemctl enable social-media-app
```

Check the service status:

```bash
sudo systemctl status social-media-app
```

## Useful Commands

Restart the app after pulling new code:

```bash
sudo systemctl restart social-media-app
```

View logs:

```bash
sudo journalctl -u social-media-app -f
```

Show the latest logs:

```bash
sudo journalctl -u social-media-app --no-pager -n 50
```

## Troubleshooting

If the API is not reachable, check whether the service is running:

```bash
sudo systemctl status social-media-app
```

Check whether the app is listening on port `8000`:

```bash
ss -tulpen | grep 8000
```

If SQLite cannot open the database file, fix the project directory permissions:

```bash
sudo chown -R ssm-user:ssm-user /opt/social-media-app
```

If Uvicorn cannot import `main`, use the correct module path:

```bash
python -m uvicorn web_app.main:app --host 0.0.0.0 --port 8000
```

If port `8000` is already in use, stop old Uvicorn processes or restart the service:

```bash
sudo pkill -f uvicorn
sudo systemctl restart social-media-app
```

## Deployment Workflow

Typical deployment steps:

```bash
cd /opt/social-media-app
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart social-media-app
sudo systemctl status social-media-app
```

Verify the API afterwards:

```text
http://<EC2_PUBLIC_IP>:8000/docs
```
