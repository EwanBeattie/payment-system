# Accesses and alters the database. This should be the only class that does this.
# This class should only be called from schema.py
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from database.models import User, Transaction, Base, engine
# from schema.schema import engine

# DATABASE_URL = "postgresql://postgres:rootpassword@localhost:5432/postgres"
DEFAULT_STARTING_BALANCE = 1000.0
#
# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(bind=engine)
#
# @contextmanager
# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#         session.commit()
#     except Exception as exception:
#         session.rollback()
#         raise exception
#     finally:
#         session.close()

# Tables
def initialise_tables():
    Base.metadata.create_all(engine)

def initialise_table(table):
    table.__table__.create(engine)

def destroy_table(table):
    table.__table__.drop(engine)

def destroy_all_tables():
    Base.metadata.drop_all(engine)

# Users
def create_user(username:str, password:str, session):
    new_user = User(username=username, password=password, balance=DEFAULT_STARTING_BALANCE)
    session.add(new_user)
    print('User created')

def get_users(session):
    users = session.query(User).all()
    return users

# This method can return a null value showing there is no user by that name
def get_user(username, session):
    user = session.query(User).filter_by(username=username).one_or_none()
    return user

def delete_user(user, session):
    session.delete(user)

def delete_all_users(session):
    users = get_users(session)
    for user in users:
        delete_user(user, session)

def delete_user_by_id(unique_id, session):
    user = session.query(User).filter_by(id=unique_id).one_or_none()
    session.delete(user)

# Auth
def verify_password(username, password, session):
    user = get_user(username, session)
    return user.password == password

# Transactions
def create_transaction(amount, dateTime, payer, recipient, session):
    new_transaction = Transaction(amount=amount,
                                  dateTime=dateTime,
                                  payer_id=payer.id,
                                  payer_username=payer.username,
                                  recipient_username=recipient.username,
                                  recipient_id=recipient.id)
    session.add(new_transaction)

    return new_transaction

def get_transaction(transaction_id, session):
    transaction = session.query(User).filter_by(id=transaction_id).one_or_none()

    if transaction is None:
        raise ReferenceError(f'{get_transaction.__name__} is returning a null value!')

    return transaction

def execute_transaction(payer, recipient, amount):
    payer.balance -= amount
    recipient.balance += amount