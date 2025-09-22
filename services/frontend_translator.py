# Here we translate the requests that come from the frontend into GraphQL format.
import schema.schema as schema

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

    result = schema.execute(mutation)

    return {'data': result.data['attemptLogin']['loginSuccess'] if not result.errors else None,
            'errors': result.errors}

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

    result = schema.execute(add_user_mutation)

    return {'data': result.data['addUser']['user'] if not result.errors else None,
            'errors': result.errors}

def delete_user(username):
    delete_user_mutation = f'''
    mutation {{
      deleteUser(username: "{username}") {{
        isDeleted
      }}
    }}
    '''

    result = schema.execute(delete_user_mutation)

    return {'data': result.data['deleteUser']['isDeleted'] if not result.errors else None,
            'errors': result.errors}

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
    result = schema.execute(get_users)

    return {'data': result.data['getUsers'] if not result.errors else None,
            'errors': result.errors}

def get_user(username):
    get_user = f'''
    query {{
      getUser(username: "{username}") {{
        id
        username
        balance
      }}
    }}
    '''
    result = schema.execute(get_user)

    return {'data': result.data['getUser'] if not result.errors else None,
            'errors': result.errors}

def get_transactions(username):
    get_transactions = f'''
    query {{
      getUser(username: "{username}") {{
        paymentsMade {{
          id
          amount
          dateTime
          payerUsername
          recipientUsername
        }}
        paymentsReceived {{
          id
          amount
          dateTime
          payerUsername
          recipientUsername
        }}
      }}
    }}
    '''
    result = schema.execute(get_transactions)

    return {'data': result.data['getUser'] if not result.errors else None,
            'errors': result.errors}

def request_transaction(amount, payer_username, recipient_username):
    request_transaction = f'''
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

    result = schema.execute(request_transaction)
    
    return {'data': result.data['requestTransaction'] if not result.errors else None,
            'errors': result.errors}