from sqlalchemy import create_engine, Column, Integer, String
from app.database import Base

# This is the User model which represents the users table in our database. It has three columns: id, username, and hashed_password. 

class User(Base):
    __tablename__ = 'users' # Name of the table in the database.
    
    id = Column(
        Integer, primary_key=True, index=True
    )
    
    username = Column(
        String, nullable=False
    )
    
    email = Column(
        String, nullable=False, unique=True
    )
    
    password = Column(
        String, nullable=False
    )