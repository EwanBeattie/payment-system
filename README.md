# Wave Payment System

## Project Overview
This project is to get hand-on experience with the following tools:
- GraphQL (graphene)
- PostgreSQL (sqlalchemy)
- Flask

## Architecture
![Showing the project's overall architecture](architecture.png)
## Features

## Installation
- Clone the git repo
- Run 'pip install -r requirements'
- Run app.py

## GraphQL Schema
See 'schema.graphql'

## ToDo
- Error handling: I need to make the frontend_translator correcly handle all errors that come from the GraphQL API. Maybe I should have an error page that it loads.
- There is no password check at login
- We do not correctly display 'Incorrect username message' to the user
- Password security: we currently have it in the URL of the userpage
- We should hash the passwords
- Add typechecks

