import database_manager

def createNewUser(username:str, password:str):
    database_manager.create_user(username, password)
