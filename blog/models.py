from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="blogs")

    # def __repr__(self):
    #    return "<Blog(title='%s', body='%s')>" % (
    #                         self.title, self.body)

class User(Base):
   
    __tablename__='users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="owner")
