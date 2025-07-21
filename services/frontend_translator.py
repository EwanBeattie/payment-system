# Here we simulate the GraphQL requests that come from the frontend.
import schema.schema

def attempt_login(username, password):
    mutation = f'''
    mutation 
    {{
      attemptLogin(username: "{username}" password: "{password}") 
      {{
        loginSuccess
      }}
    }}
    '''

    result = schema.schema.execute(mutation)
    return result

def add_user(username, password):
    add_user_mutation = f'''
    mutation {{
      addUser(username: "{username}" password: "{password}") {{
        user {{
          username
          password
          balance
        }}
      }}
    }}
    '''

    result = schema.schema.execute(add_user_mutation)
    return result

def delete_user(username):
    delete_user_mutation = f'''
    mutation {{
      deleteUser(username: "{username}") {{
        isDeleted
      }}
    }}
    '''

    result = schema.schema.execute(delete_user_mutation)
    return result

def get_users():
    get_users = '''
    query {
      getUsers {
        id
        username
        password
        balance
      }
    }
    '''
    result = schema.schema.execute(get_users)
    if result.errors:
        print(f"Errors: {result.errors}")
        return None
    else:
        data = result.data['getUsers']
        return data

def get_user(username):
    get_user = f'''
    query {{
      getUser(username: "{username}") {{
        id
        username
        password
      }}
    }}
    '''
    result = schema.schema.execute(get_user)
    if result.errors:
        print(f"No user found with username: {username}\nErrors: {result.errors}")
        return None
    else:
        data = result.data['getUser']
        return data

def request_transaction(amount, payer_username, recipient_username):
    request_transaction_mutation = f'''
    mutation {{
      requestTransaction(amount: {amount} payerUsername: "{payer_username}" recipientUsername: "{recipient_username}") {{
        transaction {{
          amount
          dateTime
          payerUsername
          recipientUsername
          payerId
          recipientId
        }}
      }}
    }}
    '''
    
    result = schema.schema.execute(request_transaction_mutation)
    return result