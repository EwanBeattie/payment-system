import datetime
import database.database as database
from graphql import GraphQLError

def request_transaction(amount, payer_username, recipient_username, session):
    payer = database.get_user(payer_username, session)
    recipient = database.get_user(recipient_username, session)

    # TODO: Can this error be moved into the schema class
    if payer is None:
        raise GraphQLError('Could not find payer in database')
    if recipient is None:
        raise GraphQLError('Could not find recipient in database')

    # Raise transaction request
    dateTime = datetime.time()
    new_transaction = database.create_transaction(amount, dateTime, payer, recipient, session)

    # Check payer has enough money in account
    if payer.balance < amount:
        # TODO: set transaction to failed
        raise GraphQLError('Payer does not have enough funds in their account')

    # Transfer money
    # Debug
    print(f'payer {payer.balance}')
    print(f'recipient {recipient.balance}')

    database.execute_transaction(payer, recipient, amount)
    # TODO: Set transaction to successful

    # Debug
    payer = database.get_user(payer_username, session)
    recipient = database.get_user(recipient_username, session)
    print(f'payer {payer.balance}')
    print(f'recipient {recipient.balance}')

    return new_transaction