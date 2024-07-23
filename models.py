from database import base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class User(base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)
    phone_number = Column(String)

class Todo(base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    ownerid = Column(Integer, ForeignKey('users.id'))
    