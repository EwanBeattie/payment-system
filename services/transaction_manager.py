import datetime
import database.database as database
from graphql import GraphQLError

def get_transactions(username, session):
    return database.get_transactions(username, session)

def request_transaction(amount, payer_username, recipient_username, session):
    payer = database.get_user(payer_username, session)
    recipient = database.get_user(recipient_username, session)

    # TODO: Can this error be moved into the schema class
    if payer is None:
        raise GraphQLError('Could not find payer in database')
    if recipient is None:
        raise GraphQLError('Could not find recipient in database')
    if payer == recipient:
        raise GraphQLError('You cannot pay yourself')

    # Raise transaction request
    dateTime = datetime.datetime.now().strftime('%d/%m/%y %H:%M')
    new_transaction = database.create_transaction(amount, dateTime, payer, recipient, session)

    # Check payer has enough money in account
    if payer.balance < amount:
        raise GraphQLError('You do not have enough funds in your account')

    # Transfer money
    database.execute_transaction(payer, recipient, amount)

    return new_transaction