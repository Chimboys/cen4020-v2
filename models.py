from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base  # 
from sqlalchemy.ext.declarative import declarative_base
from database import engine

metadata = MetaData()
 #creating a base class

class User(Base): #creating a class User
    __tablename__ = "users" #name of the table
    id = Column(Integer, primary_key=True, index=True) #creating a column id
    username = Column(String, unique=True, nullable=False, index=True) #creating a column email
    hashed_password = Column(String, nullable=False) #creating a column hashed_password
    school = Column(String, nullable=False) #creating a column school
    created_at = Column(TIMESTAMP, server_default=text('now()')) #creating a column created_at
    first_name = Column(String, unique=True, nullable=False) #creating a column first_name
    last_name = Column(String, unique=True, nullable=False) #creating a column last_name



class Friendship(Base):
    __tablename__ = "friendships"
    user_id = Column(Integer, ForeignKey('users.id',  ondelete='CASCADE'), primary_key=True)
    friend_id = Column(Integer, ForeignKey('users.id',  ondelete='CASCADE'), primary_key=True)
    declared_at = Column(TIMESTAMP, server_default=text('now()')) #creating a column created_at

    # Define relationships
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])
    # Define a composite primary key constraint
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'friend_id'),
    )

Base.metadata.create_all(engine) #creating the table