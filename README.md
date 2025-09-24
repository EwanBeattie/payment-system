# Wave Payment System

## Project Overview
Hello,

Welcome to my simple payment system. I built this to strengthen my application to Wave and have used the following technologies:

- Backend & API: Python, GraphQL, Graphene, Flask, SQLAlchemy
- Database: PostgreSQL
- Server & Deployment: Hetzner (hosting), Linux (server OS), SSH (secure access), Gunicorn (WSGI server)
- Frontend: JavaScript, HTML, and CSS (AI-assisted)

All backend and server code was written by me; the frontend was generated with AI assistance.

## Architecture
![Showing the project's overall architecture](architecture.png)
## Features

<!-- ## Installation
- Clone the git repo
- Run 'pip install -r requirements'
- Run app.py -->

## Remote Server
- Clone the repo
- Make sure you have python and pip
```sudo apt update && sudo apt install -y python3 python3-venv python3-pip```
- Create and activate your venv file
```python3 -m venv venv```
```source .venv/bin/activate```
- Install requirements
```pip install -r requirements.txt```

- Install postgreSQL
```sudo apt install -y postgresql```
- Make your postgreSQL account and update the code with the relevant credentials


## Gunicorn Setup
- Add a service file to /etc/systemd/system/payment-system.service
<code>[Unit]
Description=Gunicorn instance for payment-system
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/payment-system
Environment="PATH=/root/payment-system/.venv/bin"
ExecStart=/root/payment-system/.venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target<code>

Where the ExecStart path points to module_name:flask_instance_name, both called app in my case (app.py/app = Flask(__name__))


## Linux Controls
To use Gunicorn to keep the server running the flask app as a systemd service we use:
```sudo systemctl start payment-system```	Start a service immediately
```sudo systemctl stop payment-system```	Stop a running service
```sudo systemctl restart payment-system```	Stop & start a service (reload)
```sudo systemctl enable payment-system```	Start the service automatically at boot
```sudo systemctl disable payment-system```	Prevent the service from starting at boot
```sudo systemctl status payment-system```	Show whether the service is running and logs
```sudo systemctl daemon-reload```	        Reload systemd after editing service files


## GraphQL Schema
See ```schema/schema.graphql```

## Desired Improvements
- I want to make a distinction between developer error messaging and user messaging. Currently they go through the same channels and display in the same place in the UI.

## ToDo
- Add description to the home page
- Add mypy typechecks
- Comment code
- Back to homepage button (logout)
- Can just type URL to get behind login screen
- Update schema.graphql
- Clean up front end html files
- Everytime we access the frontend_translator we have to check if the API came back with errors. We could automate this (see app.py)
- We only ever display the first error, this seems fine for this application for now

