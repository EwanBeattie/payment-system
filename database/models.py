# This script defines the database models (i.e. database tables and their relationships)

# ORM (Object-Relational Mapping) is a programming technique that lets you interact with your database using Python objects instead of writing raw SQL queries.

# Without ORM (raw SQL):
# SELECT * FROM users WHERE username = 'john';
# INSERT INTO transactions (amount, payer_id) VALUES (100.0, 1);

# With ORM (Python objects):
# user = session.query(User).filter_by(username='john').first()
# transaction = Transaction(amount=100.0, payer_id=1)

from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env
db_password = os.getenv("DATABASE/_PASSWORD")

DATABASE_URL = f"postgresql://waveuser:{db_password}@localhost:5432/wave"

# DATABASE_URL = "postgresql://postgres@localhost:5432/wave"

# TODO: Move this to database.py
# Thie creates the connection to the database
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")

# declarative_base() is a SQLAlchemy factory function that creates a base class for all your ORM models.
Base = declarative_base()
# Base.metadata
# The Base object contains a metadata attribute that tracks all your tables:
# # This creates all tables in your database
# Base.metadata.create_all(engine)
# # This drops all tables
# Base.metadata.drop_all(engine)

# TODO: Add this
# class TransactionStatus(enum.Enum):
#     PENDING = "pending"
#     COMPLETED = "completed"
#     FAILED = "failed"
#     REFUNDED = "refunded"
#     CANCELLED = "cancelled"

#     status = Column(enum.Enum(TransactionStatus), nullable=False)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    dateTime = Column(String, nullable=False)
    payer_username = Column(String, nullable=False)
    recipient_username = Column(String, nullable=False)

    payer_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))

    # N.B. If you use backref you don't need to define the other side of the relationship
    payer = relationship("User", foreign_keys=[payer_id], back_populates="payments_made")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="payments_received")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)

    payments_made = relationship("Transaction",
                                 foreign_keys="[Transaction.payer_id]",
                                 back_populates="payer")
    payments_received = relationship("Transaction",
                                     foreign_keys="[Transaction.recipient_id]",
                                     back_populates="recipient")