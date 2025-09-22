# Accesses and alters the database. This should be the only class that does this.
# This class should only be called from schema.py
from database.models import User, Transaction, Base, engine

DEFAULT_STARTING_BALANCE = 1000.0

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
    username = str.lower(username)
    new_user = User(username=username, password=password, balance=DEFAULT_STARTING_BALANCE)
    session.add(new_user)
    return(new_user)

# def get_users(session):
#     users = session.query(User).all()
#     return users

def get_users(session):
    try:
        users = session.query(User).all()
        return users
    except Exception as e:
        # TODO: Correctly display error
        print(f"Error fetching users: {e}")
        return []

# This method can return a null value showing there is no user by that name
def get_user(username, session):
    username = str.lower(username)
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

def get_transactions(username, session):
    user = get_user(username, session)
    payments_made = session.query(Transaction).filter_by(payer_id=user.id).all()
    payments_received = session.query(Transaction).filter_by(recipient_id=user.id).all()
    return {'payments_made': payments_made,
            'payments_received': payments_received}

def get_transaction(transaction_id, session):
    transaction = session.query(User).filter_by(id=transaction_id).one_or_none()
    return transaction

def execute_transaction(payer, recipient, amount):
    payer.balance -= amount
    recipient.balance += amount