import re  
import hashlib
from user import UserCreate
import models
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.sql import func

def check_password(password):
    # Check if password meets the requirements
    if len(password) < 8 or len(password) > 12:
        print("Password must be between 8 and 12 characters.")
        return False
    if not re.search(r'[A-Z]', password):
        print("Password must contain at least one capital letter.")
        return False
    if not re.search(r'\d', password):
        print("Password must contain at least one digit.")
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        print("Password must contain at least one special character.")
        return False
    return True

def signup(db):
    # Get user input
    has_account = input("Do you already have an account? (yes/no): ")
    if has_account.lower() == 'yes':
        login(db)
        return

    username = input("Enter your username: ")
    school = input("Enter your school: ")
    hashed_password = input("Enter your password: ")
    

    # Check password
    if check_password(hashed_password):
        #Checking amount of users
        if db.query(func.count(models.User.id)).scalar() > 5:
            print("You have reached the maximum number of users.")
            continue_signup = input("Would you like to login instead? (yes/no)")
            if continue_signup.lower() == 'yes':
                login(db)
            return
        if db.query(models.User).filter(models.User.username == username).first():
            print("Username already in use.")
            continue_signup = input("Would you like to login instead? (yes/no)") #change
            if continue_signup.lower() == 'yes':
                login(db)
            return
        user_create = UserCreate(username=username, hashed_password=hashed_password, school=school)
        new_user = models.User(**user_create.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("User created successfully")
        print("Account created successfully!")

    else:

        continue_signup = input("Password is invalid. Do you want to continue signup? (yes/no): ")
        if continue_signup.lower() == 'yes':
            signup(db)
        else:
            print("Signup cancelled.")
            return

def login(db):
    # Get user input
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if not check_password(password):
        continue_signup = input("Password is invalid. Do you want to continue login? (yes/no): ")
        if continue_signup.lower() == 'yes':
            login(db)
        else:
            print("Login cancelled.")
        return

    
    queryUser = db.query(models.User).filter(models.User.username == username).first()
    if queryUser is None:
        print("Sigh Up first")
        return
    elif queryUser.hashed_password != password:
        print("Password is incorrect")
        return
    print("Login successfulyes")
    print(queryUser.id)



db = next(get_db())
try:
    signup(db)
finally:
    db.close()