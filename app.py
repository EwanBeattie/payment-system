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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        action = request.form['action']

        if action == 'login':
            # TODO: Add password check
            # TODO: Correctly display 'no user by this name' message
            result = frontend_translator.attempt_login(username, password)
        elif action == 'create':
            user = frontend_translator.get_user(username)
            if user is None:
                result = frontend_translator.add_user(username, password)
            else:
                return render_homepage(error="User already exists")
        
        print(result)
        if result.errors:

            return 'Did not work' + str(result.errors)

        return redirect(url_for('user_page', user=username, password=password))

        # To get all the data
        # dictio = request.form.to_dict()
    elif request.method == 'GET':
        return render_template("index.html")

@app.route('/user/<user>/<password>')
def user_page(user, password):
    # return f'<h1>{user}, {password}</h1>'
    users = frontend_translator.get_users()
    usernames = [user['username'] for user in users]
    return render_template('wallet.html', usernames=usernames)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

def render_homepage(error=None):
    users = frontend_translator.get_users()
    usernames = [user['username'] for user in users]
    return render_template("index.html", usernames=usernames, error=error)

if __name__ == "__main__":
    database.initialise_tables() 
    app.run(debug=True)
