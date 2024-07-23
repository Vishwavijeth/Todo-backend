from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todoApp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autoflush= False)

base = declarative_base()
