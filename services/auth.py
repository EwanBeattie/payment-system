# Authentication manager
from graphql import GraphQLError
import database.database as database
from passlib.context import CryptContext 

password_hasher = CryptContext(schemes=["argon2"], deprecated="auto")

def attempt_login(username, plain_text_password, session):

    user = database.get_user(username, session)
    if user is None:
        raise GraphQLError('Username is not in the database')

    return verify_password(plain_text_password, user.password)

def hash_password(plain_text):
    return password_hasher.hash(plain_text)

def verify_password(plain, hashed):
    return password_hasher.verify(plain, hashed)