from flask import Flask, render_template, request, url_for, redirect
from flask_graphql import GraphQLView
from flask_cors import CORS
from database import database
from schema.schema import schema
import services.frontend_translator as frontend_translator

app = Flask(__name__, template_folder="front_end/templates", static_folder="front_end/static")
CORS(app)  # Enable CORS for frontend communication

@app.route('/')
def home():
    return render_homepage()

@app.route('/start', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        username = str.lower(request.form['name'])
        password = str.lower(request.form['password'])
        action = request.form['action']

        if action == 'login':
            return login(username, password)
        elif action == 'create':
            return create_account(username, password)

    elif request.method == 'GET':
        return render_homepage()

@app.route('/user/<username>')
def user_page(username):
    return render_wallet(username)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

# Route to handle payment form submission
@app.route('/make_payment', methods=['POST'])
def make_payment():
    username = str.lower(request.form['username'])
    recipient = str.lower(request.form['recipient'])
    amount = request.form['amount']

    amount = float(amount)
   
    result = frontend_translator.request_transaction(amount, username, recipient)
    if result['errors']:
        return render_wallet(username, error=result['errors'][0].message)

    return redirect(url_for('user_page', username=username))

def render_homepage(error=None):
    result = frontend_translator.get_users()

    if result['errors']:
        users = []

        if error is None:
            error = result['errors']

    else:
        users = result['data']

    usernames = [user['username'] for user in users]
    return render_template("index.html", usernames=usernames, error=error)

def render_wallet(username, error=None):
    result = frontend_translator.get_users()
    users = result['data']

    if result['errors']:
        return render_wallet_with_error(result['errors'][0].message)

    usernames = [user['username'] for user in users]
    usernames.remove(username)

    # TODO: Check for errors
    user = frontend_translator.get_user(username)['data']
    balance = user['balance']

    result = frontend_translator.get_transactions(username)
    if result['errors']:
        return render_wallet_with_error(result['errors'])
    
    transactions = result['data']
    
    if transactions is not None:
        payments_made = transactions['paymentsMade']
        for outgoing_payment in payments_made:
            outgoing_payment.update({'type':'outgoing'})

        payments_received = transactions['paymentsReceived']
        for incoming_payment in payments_received:
            incoming_payment.update({'type':'incoming'})
        
        all_transactions = payments_made + payments_received
        all_transactions.sort(key=lambda x: int(x['id']), reverse=True)

    return render_template('wallet.html', 
                           username=username, 
                           transactions=all_transactions,
                           usernames=usernames, 
                           balance=balance, 
                           error=error)

def render_wallet_with_error(error):
    return render_template('wallet.html', 
                        username='null', 
                        transactions=[],
                        usernames=[], 
                        balance='0', 
                        error=error)

def login(username, password):
    result = frontend_translator.attempt_login(username, password)

    if result['errors']:
        return render_homepage(error=result['errors'][0].message)
    
    loginSuccess = result['data']

    if not loginSuccess:
        return render_homepage(error='Incorrect password')
        
    return redirect(url_for('user_page', username=username))

def create_account(username, password):
    result = frontend_translator.get_user(username)

    if result['errors']:
        return render_homepage(error=result['errors'][0].message)
    user = result['data']
    
    if user is None:
        result = frontend_translator.add_user(username, password)
        if result['errors']:
            return render_homepage(error=result['errors'][0].message)
        
    else:
        return render_homepage(error="User already exists")
    
    return redirect(url_for('user_page', username=username))    

if __name__ == "__main__":
    database.initialise_tables() 
    app.run(host="0.0.0.0", port=5000, debug=True)

    # app.run(debug=True)
