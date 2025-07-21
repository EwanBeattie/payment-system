from graphql import GraphQLError
import database.database as database

def get_user(username, session):
    return database.get_user(username, session)

def get_users(session):
    return database.get_users(session)

def add_user(username, password, session):
    if database.get_user(username, session):
        raise GraphQLError("Username already exists")
    database.create_user(username, password, session)
    # Alternative way, this double checks the user is in and retrievable from the database
    new_user = database.get_user(username, session)
    return new_user

def delete_user(username, session):
    user = database.get_user(username, session)
    if user is None:
        raise GraphQLError('No user by this username was found')
    database.delete_user(user, session)
    deleted_user = database.get_user(username, session)
    return deleted_user

