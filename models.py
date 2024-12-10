from sqlalchemy import Integer,String,Boolean,Column,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Blogs(Base):
    __tablename__="blog"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(100),nullable=False)
    body=Column(String(300),nullable=False)
    user_id=Column(Integer,ForeignKey("user.id"))

    creator=relationship("User",back_populates="blogs")

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True) 
    username=Column(String(100),nullable=False)
    email=Column(String(200),unique=True,nullable=False)   
    password=Column(String(300),nullable=False)

    blogs=relationship("Blogs",back_populates="creator")
