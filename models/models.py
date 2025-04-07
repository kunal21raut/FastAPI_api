

from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blog"

    id  = Column(Integer,primary_key=True, index=True)
    title = Column(String(80), nullable=False)
    content = Column(String(500), nullable=False)
    author = Column(String(50), nullable=False)
    is_published = Column(Boolean, default=False)

    user_id = Column(String, ForeignKey('users.userid'))

    owner = relationship('User',back_populates='blogs')


    class Config:
        orm_mode = True

    
class User(Base):
    __tablename__ = "users"

    userid = Column(String(50),primary_key=True,index=True)
    username = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    password = Column(String(100),nullable=False)


    blogs = relationship('Blog', back_populates='owner')