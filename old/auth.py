import database_manager

def authenticateUser(username:str, password:str):
    return database_manager.verify_password(username, password)

def checkUniqueUser(username:str):
    users = database_manager.get_users()
    for user in users:
        if user.username == username:
            return False

    return True
