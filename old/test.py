import graphene

# Define User type
class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    password = graphene.String()
    balance = graphene.Float()

# Define Transaction type
class Transaction(graphene.ObjectType):
    payer = graphene.Field(User)
    recipient = graphene.Field(User)
    amount = graphene.Float()
    datetime = graphene.DateTime()

# Query class with all_users field
class Query(graphene.ObjectType):
    all_users = graphene.List(User)

    def resolve_all_users(self, info):
        # Mock data (replace with database query)
        return [
            User(id=1, username="Alice", password="hashed1", balance=100.0),
            User(id=2, username="Bob", password="hashed2", balance=50.0),
        ]

# Create schema
schema = graphene.Schema(query=Query)

# Example query
query_string = "{ allUsers { id username } }"
result = schema.execute(query_string)
print(result.data)
