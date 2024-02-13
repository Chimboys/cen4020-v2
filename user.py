# Import the BaseModel class from the pydantic module
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):  # creating a class User
    username: str  # creating a variable email
    hashed_password: str  # creating a variable hashed_password
    school: str  # creating a variable school
    first_name: str
    last_name: str


class UserInfo(BaseModel):
    id: int
    username: str
    school: str
    first_name: str
    last_name: str


class Friends(BaseModel):
    user_id: int
    friend_id: int
