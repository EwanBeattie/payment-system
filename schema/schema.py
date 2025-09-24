# The schema defines what data can be access and changed. If a mutation is called, the schema
# calls the database.py to perform the change

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from sqlalchemy.orm import sessionmaker

import services.auth
from database.models import User, Transaction, engine
from services import transaction_manager, user_manager

DEFAULT_STARTING_BALANCE = 1000.0

SessionLocal = sessionmaker(bind=engine, autoflush=True)

# Types
class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User

    payments_made = graphene.List(lambda: TransactionType)
    payments_received = graphene.List(lambda: TransactionType)

    def resolve_payments_made(parent, info):
        return parent.payments_made

    def resolve_payments_received(parent, info):
        return parent.payments_received

class TransactionType(SQLAlchemyObjectType):
    class Meta:
        model = Transaction



# Queries
class Query(graphene.ObjectType):
    get_user = graphene.Field(UserType, username=graphene.String())
    get_users = graphene.List(UserType)
    get_transactions = graphene.List(UserType, username=graphene.String())

    def resolve_get_user(self, info, username):
        session = info.context.get('session')
        user = user_manager.get_user(username, session)
        return user
    
    def resolve_get_users(self, info):
        session = info.context.get('session')
        users = user_manager.get_users(session)
        return users



# Mutations
class AddUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, username, password):
        session = info.context.get('session')
        new_user = user_manager.add_user(username, password, session)
        return AddUser(user=new_user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    is_deleted = graphene.Boolean()

    def mutate(self, info, username):
        session = info.context.get('session')
        user = user_manager.delete_user(username, session)
        return DeleteUser(is_deleted=user is None)

class RequestTransaction(graphene.Mutation):
    class Arguments:
        amount = graphene.Float()
        payer_username = graphene.String()
        recipient_username = graphene.String()

    transaction = graphene.Field(TransactionType)

    def mutate(self, info, amount, payer_username, recipient_username):
        session = info.context.get('session')
        new_transaction = transaction_manager.request_transaction(amount, payer_username, recipient_username, session)
        return RequestTransaction(transaction=new_transaction)

class AttemptLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    login_success = graphene.Boolean()

    def mutate(self, info, username, password):
        session = info.context.get('session')
        success = services.auth.attempt_login(username, password, session)
        return AttemptLogin(login_success=success)

# This is an example to help demonstarte what each section does.
class ExampleMutation(graphene.Mutation):
    # You place whatever arguments are required to carry out the mutation here
    class Arguments:
        example_arg = graphene.String(required=True)
        another_arg = graphene.Int()

    # This is what the mutation will return
    success = graphene.Boolean()

    # This is where you perform the mutation logic (called the resolver), often in 
    # the form of calling your backend script 
    def mutate(self, info, example_arg):
        print(f"Example mutation called with argument: {example_arg}")
        return ExampleMutation(success=True)



# Defines all the mutations
class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()
    delete_user = DeleteUser.Field()
    request_transaction = RequestTransaction.Field()
    attempt_login = AttemptLogin.Field()
    example_mutation = ExampleMutation.Field()


# Initialise the schema
schema = graphene.Schema(query=Query, mutation=Mutation)


# These functions are only ones to call mutations
def execute_with_variable(mutation, variables):
    result = schema.execute(mutation, variables=variables)
    print(result)

def execute(mutation, variables = None):
    # Make a new session per mutation
    session = SessionLocal()

    try:
        # Include session in context. We need to pass it along to the database
        context = {'session': session}
        if variables is None:
            result = schema.execute(mutation, context_value=context)
        else:
            result = schema.execute(mutation, variables=variables, context_value=context)

        # Check if there were errors in the GraphQL execution
        if not result.errors:
            session.commit()
        else:
            # Roll back if there were GraphQL errors
            session.rollback()

        return result

    except Exception as exception:
        # Roll back if there was an exception
        session.rollback()
        raise exception

    finally:
        session.close()