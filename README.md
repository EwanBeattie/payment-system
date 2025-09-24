# Wave Payment System

Currently hosted on: http://94.130.78.58:5000/

## Project Overview
Hello,

Welcome to my simple payment system. I built this to strengthen my application to Wave and have used the following technologies:

- **Backend & API**: Python, GraphQL, Graphene, Flask, SQLAlchemy
- **Database**: PostgreSQL
- **Server & Deployment**: Hetzner (hosting), Linux (server OS), SSH (secure access), Gunicorn (WSGI server)
- **Frontend**: JavaScript, HTML, and CSS (AI-assisted)

All backend and server code was written by me; the frontend was generated with AI assistance.

## Architecture
![Showing the project's overall architecture](architecture.png)
## Features

User Management
* User registration (create account): Users can create new accounts with a username and password.
* User login: Users can log in with their credentials; passwords are securely hashed using Argon2.
* User authentication: Passwords are verified securely; login attempts are validated against the database.
* User listing: The homepage displays a list of all current users.

Wallet & Account
* User wallet page: Each user has a wallet page showing their balance and transaction history.

Payments & Transactions
* Make payments: Users can send payments to other users (cannot pay themselves).
* Transaction validation: Checks for sufficient funds before processing payments.
* Transaction history: Users can view their sent and received payments, including amount, date/time, payer, and recipient.
* Transaction creation: Each payment creates a transaction record in the database.
* Transaction listing: Both payments made and received are shown in the wallet.

Backend & API
* GraphQL API: Exposes queries and mutations for user and transaction management.
* Flask backend: Handles routing, rendering templates, and serving the GraphQL endpoint.
* CORS enabled: Allows frontend and backend to communicate securely.

Security
* Passwords are hashed using Argon2 (via passlib).
* Error handling for invalid login, duplicate usernames, insufficient funds, and invalid transactions.

Database
* SQLAlchemy ORM models for users and transactions.
* PostgreSQL database connection (with .env support for credentials).
* Database initialisation and table management functions.

Other Features
* Session management for database operations.
* Modular code structure: clear separation of concerns (auth, user management, transactions, frontend translation, database access).

## GraphQL Schema
See ```schema/schema.graphql```

## Project Set-Up
If you want to, I have provided the instructions on how to get this project up and running on your own server. These are mainly for my benefit when I want to rememeber how I did it.

### Connect to your server
- Get a server (I used Hetzner)
- Set it up with a private key for auth

```ssh-keygen -t ed25519 -C "project_name"```

- Add a config file to you ./ssh folder
```
Host <server_name>  
  HostName xx.xxx.xx.xx  
  User root  
  IdentityFile ~/.ssh/<private_key_file>  
```
- You should now be able to access the server with the command

```ssh <server_name>```

### Installation
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

### Gunicorn Setup
Gunicorn allows us to keep the server running our app after we close the shell and logout.
- Add a service file to ```/etc/systemd/system/payment-system.service```

```
[Unit]
Description=Gunicorn instance for payment-system
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/payment-system
Environment="PATH=/root/payment-system/.venv/bin"
ExecStart=/root/payment-system/.venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Where the ExecStart path points to ```module_name:flask_instance_name```, both called app in my case ```app.py``` and ```app = Flask(__name__)```


### Linux Controls
To use Gunicorn to keep the server running the flask app as a systemd service we use:  
```sudo systemctl start payment-system```	Start a service immediately  
```sudo systemctl stop payment-system```	Stop a running service  
```sudo systemctl restart payment-system```	Stop & start a service (reload)  
```sudo systemctl enable payment-system```	Start the service automatically at boot  
```sudo systemctl disable payment-system```	Prevent the service from starting at boot  
```sudo systemctl status payment-system```	Show whether the service is running and logs  
```sudo systemctl daemon-reload```	        Reload systemd after editing service files  



## Desired Improvements
- I want to make a distinction between developer error messaging and user messaging. Currently they go through the same channels and display in the same place in the UI
- When paying someone, I want to select their user tile, not have to type the name
- Create a 'Back To Homepage' or 'Logout' button
- Everytime we access the frontend_translator we have to check if the API came back with errors. We could automate this (see app.py)

## ToDo
- Add mypy typechecks
- Comment code and clean up

## Bugs
- No restrictions on usernames (e.g. can be blank or spaces). Blank username breaks webpage
- Can type URL to get behind login screen & into someone's account
- We only ever display the first GraphQL error, this seems fine for this application for now
- You can pay yourself by making a payment with a negative number



