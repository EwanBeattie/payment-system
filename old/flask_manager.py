# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route('/')
# def homepage():
#     return 'Hello world'
#
# if __name__ == '__main__':
#     app.run()
import auth
import user_manager


# Load the home page
# Link up the button presses to the relevant functions

def sign_in(username, password):
    if auth.authenticateUser(username, password):
        print('You have successfully signed in')
        # TODO: Load next webpage
    else:
        print('Incorrect password')

def register(username, password):
    if auth.checkUniqueUser(username):
        print('Your username is unique')
        user_manager.createNewUser(username, password)
    else:
        print('Username already in use')

        # TODO: Load next webpage

# register('ewan', 'password')
# delete_user('ewan')
sign_in('ewan', 'fdc')
