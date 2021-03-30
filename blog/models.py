from sqlalchemy import Column, Integer, String
from .database import Base

class Blog(Base):
    
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    # def __repr__(self):
    #    return "<Blog(title='%s', body='%s')>" % (
    #                         self.title, self.body)

class User(Base):
   
    __tablename__='users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)