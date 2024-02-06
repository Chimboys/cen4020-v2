from pydantic import BaseModel, EmailStr  # Import the BaseModel class from the pydantic module

class UserCreate(BaseModel): #creating a class User
    email: EmailStr #creating a variable email
    hashed_password: str #creating a variable hashed_password
    school: str #creating a variable school