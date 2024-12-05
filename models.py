from sqlalchemy import Integer,String,Boolean,Column

from .database import Base

class Blogs(Base):
    __tablename__="blog"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(100),nullable=False)
    bbody=Column(String(300),nullable=False)