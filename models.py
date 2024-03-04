from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData, PrimaryKeyConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base  #
from sqlalchemy.ext.declarative import declarative_base
from database import engine

metadata = MetaData()
# creating a base class

class GuestControl(Base):
    __tablename__ = "guest_controls"
    id = Column(Integer, primary_key=True, index=True)
    incollege_email_enabled = Column(Boolean, default=True, nullable=False)
    sms_enabled = Column(Boolean, default=True, nullable=False)
    targeted_advertising_enabled = Column(Boolean, default=True, nullable=False)
    language_preference = Column(String, server_default="English", nullable=False)

    # Establish one-to-one relationship with User
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="guest_control")

class User(Base):  # creating a class User
    __tablename__ = "users"  # name of the table
    id = Column(Integer, primary_key=True, index=True)  # creating a column id
    username = Column(String, unique=True, nullable=False,
                      index=True)  # creating a column email
    # creating a column hashed_password
    hashed_password = Column(String, nullable=False)
    school = Column(String, nullable=False)  # creating a column school
    created_at = Column(TIMESTAMP, server_default=text(
        'now()'))  # creating a column created_at
    # creating a column first_name
    first_name = Column(String, unique=True, nullable=False)
    # creating a column last_name
    last_name = Column(String, unique=True, nullable=False)
    guest_control = relationship("GuestControl", uselist=False, back_populates="user")
    profile = relationship("UserProfile", uselist=False, back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="N/A")
    major = Column(String, default="N/A")
    university_name = Column(String, default="N/A")
    about_student = Column(Text, default="N/A")
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="profile")
    experience = relationship("Experience", back_populates="user_profile", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="user_profile", cascade="all, delete-orphan")

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    employer = Column(String, nullable=False)
    date_started = Column(String, nullable=False)
    date_ended = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"))

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    years_attended = Column(String, nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"))


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id',  ondelete='CASCADE'))
    title = Column(String, nullable=False, unique=True)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text(
        'now()'))  # creating a column created_at

    # Define relationships
    user = relationship("User")


class Friendship(Base):
    __tablename__ = "friendships"
    user_id = Column(Integer, ForeignKey(
        'users.id',  ondelete='CASCADE'), primary_key=True)
    friend_id = Column(Integer, ForeignKey(
        'users.id',  ondelete='CASCADE'), primary_key=True)
    declared_at = Column(TIMESTAMP, server_default=text(
        'now()'))  # creating a column created_at

    # Define relationships
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])
    # Define a composite primary key constraint
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'friend_id'),
    )

class ProspectiveConnection(Base):
    __tablename__ = "prospective_connections"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    caller_id = Column(Integer, ForeignKey('users.id'))
    declared_at = Column(TIMESTAMP, server_default=text('now()'))  # creating a column created_at
    receiver_id = Column(Integer, ForeignKey('users.id'))

    # Define relationships
    caller = relationship("User", foreign_keys=[caller_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    # Define a composite primary key constraint



Base.metadata.create_all(engine)  # creating the table
