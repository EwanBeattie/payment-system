from database import create_engine, Column, Integer, String, Float
from database.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "postgresql://postgres:rootpassword@localhost:5432/postgres"
DEFAULT_STARTING_BALANCE = 1000.0

engine = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, nullable=False)

def initialise_table(table):
    table.__table__.create(engine)

def destroy_table(table):
    table.__table__.drop(engine)

def create_user(username:str, password:str):
    session = SessionLocal()
    try:
        new_user = User(username=username, password=password, balance=DEFAULT_STARTING_BALANCE)
        session.add(new_user)
        session.commit()
        print('User created')
    except Exception as error:
        session.rollback()
        print(f'Error creating user: {error}')
    finally:
        session.close()

def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users

def get_user(username):
    session = SessionLocal()
    user = None
    try:
        user = session.query(User).filter_by(username=username).one()
    except Exception as error:
        print(f'Error retrieving user: {error}')
    finally:
        session.close()

    return user

def delete_user(username):
    user = get_user(username)
    session = SessionLocal()
    session.delete(user)
    session.commit()
    session.close()

def verify_password(username, password):
    user = get_user(username)
    return user.password == password

# destroy_table(User)
# initialise_table(User)
# create_user('ewan', 'password')