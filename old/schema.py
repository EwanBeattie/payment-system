import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# GraphQL User Type
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

# GraphQL Transaction Type
class Transaction(SQLAlchemyObjectType):
    class Meta:
        model = TransactionModel

# Query Class
class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_transactions = graphene.List(Transaction)

    def resolve_all_users(self, info):
        return session.query(UserModel).all()  # Query database for users

    def resolve_all_transactions(self, info):
        return session.query(TransactionModel).all()  # Query database for transactions

# Create GraphQL Schema
schema = graphene.Schema(query=Query)
