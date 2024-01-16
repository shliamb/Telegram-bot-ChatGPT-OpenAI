from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer)
    user_first_name = Column(String)
    user_last_name = Column(String)
    user_username = Column(String)
    chat_id = Column(Integer)
