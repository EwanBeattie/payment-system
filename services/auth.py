# Authentication manager
from graphql import GraphQLError
import database.database as database

def attempt_login(username, password, session):

    user = database.get_user(username, session)
    if user is None:
        raise GraphQLError('Username is not in the database')

    return database.verify_password(username, password,session)