import re  
import hashlib
from user import UserCreate, UserInfo, Friends
import models
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.sql import func
from sqlalchemy import or_

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






def find_user_by_email(email:str , db: Session):
    if db.query(models.User).filter(models.User.username == email).first():
        print("They are a part of the InCollege system")
        signup(db)
    else:
        print("They are not a part of the InCollege system")
        print("Goodbye")
 




def signup(db):
    # Get user input
    has_account = input("Do you already have an account? (yes/no): ")
    if has_account.lower() == 'yes':
        login(db)
        return
    choice = str(input("Would you like to sign up? (yes/no): "))
    if choice.lower() == 'no':
        choiceFind = str(input("Would you like to find a user by email? (yes/no): "))
        if choiceFind.lower() == 'yes':
            email = input("Enter the email of the user: ")
            find_user_by_email(email, db)
        else:
            print("Goodbye")
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
        user = UserInfo(id = new_user.id, username=new_user.username, school = new_user.school)
        main_hub(user, db)
        

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
    user = UserInfo(id = queryUser.id, username=queryUser.username, school = queryUser.school)
    main_hub(user, db)



def main_hub(userData: UserInfo, db):
     
    print(userData.id)
    print(userData.username)
    print(userData.school)
    print("Search for a job: (s) ")
    print("Find new friends: (nf)")
    print("Learn new skills: (l)")
    print("View all friends: (vf)")
    print("Logout: (lo)")
    print("Exit: (e)")
    choice = input("Enter your choice: ")
    choice = choice.lower()
    if choice == 's':
        # search_job(userData, db)
        pass
    elif choice == 'nf':
        find_new_friends(userData, db)
    elif choice == 'l':
        learn_new_skills(userData, db)
        pass
    elif choice == 'vf':
        #view_all_friends(userData, db)
        pass
    elif choice == 'lo':
        login(db)
    elif choice == 'e':
        print("Goodbye")
        return
    else:
        print("Invalid choice")
        main_hub(userData, db)

def view_all_friends(userData: UserInfo, db):
    friends = db.query(models.Friendship).filter( or_(models.Friendship.user_id == userData.id, 
                                                    models.Friendship.friend_id == userData.id)).all()
    for friend in friends:
        print(friend.friend_id)
    choice = input("Would you like to go back to the main hub? (yes/no): ")
    if choice.lower() == 'yes':
        main_hub(userData, db)
    else:
        print("Goodbye")
        return



def find_new_friends(userData: UserInfo, db):
    users = db.query(models.User).all()
    idList = []
    for user in users:
        if user.id == userData.id:
            continue
        else:
            print(f"Username: {user.username}, School: {user.school}, ID: {user.id}")
            idList.append(user.id)
    add_friends(userData, db, idList)
    

def add_friends(userData: UserInfo,  db, idList: list):
    try:
        choice = int(input("if you want to add a friend, enter the id of the user, else enter no ")) #Add try and Catch Block
        if choice not in idList:
            print("Invalid id")
        elif choice == userData.id:
            print("You cannot add yourself as a friend")
        elif ( db.query(models.Friendship).filter(models.Friendship.user_id == userData.id, models.Friendship.friend_id == choice).first() 
            or 
            db.query(models.Friendship).filter(models.Friendship.user_id == choice, models.Friendship.friend_id == userData.id).first()):
            print("Friend already added")

        else:
            friends = Friends(user_id = userData.id, friend_id = choice)
            friendship = models.Friendship(**friends.dict())
            db.add(friendship)
            db.commit()
            print("Friend added")
        
        choiceAgain = input("Do you still want to add more friends? (yes/no): ")
        if choiceAgain.lower() == 'no':
            main_hub(userData, db)
        else:
            add_friends(userData, db, idList)
            
    except ValueError:
        main_hub(userData, db)
    
     

def learn_new_skills(userData: UserInfo, db):
    print("Learn new skills")
    print("1. Python")
    print("2. Java")
    print("3. C++")
    print("4. C#")
    print("5. JavaScript")
    input("Enter your choice: ")
    print("Under contruction")
    choice = input("Would you like to go back to the main hub? (yes/no): ")
    if choice.lower() == 'yes':
        main_hub(userData, db)
    else:
        print("Goodbye")
        return
   



db = next(get_db())
try:
    signup(db)
finally:
    db.close()