from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData
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
    username = Column(String, unique=True, index=True) #creating a column email
    hashed_password = Column(String) #creating a column hashed_password
    school = Column(String) #creating a column school
    created_at = Column(TIMESTAMP, server_default=text('now()')) #creating a column created_at

Base.metadata.create_all(engine) #creating the table