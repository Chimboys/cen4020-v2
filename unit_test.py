import pytest
from unittest.mock import patch


from user import UserCreate, UserInfo, Friends
# Importing the job_actions function from jobs_func.py
from jobs_func import job_actions
from models import User, GuestControl, UserNotification, ProspectiveConnection, UserProfile, Experience, Education, Post, JobPost, Message, Friendship, JobApplication
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import sqlalchemy
from database import get_db
from sqlalchemy import delete

from main import (
    check_password,
    signup,
    learn_new_skills,
    login,
    find_user_by_first_last_name,

    find_new_friends_and_send_request, 
    send_friend_request,
)

db = next(get_db())

db.query(Friendship).delete()
db.query(JobApplication).delete()
db.query(JobPost).delete()
db.query(Post).delete()
db.query(Education).delete()
db.query(Experience).delete()
db.query(Message).delete()
db.query(ProspectiveConnection).delete()
db.query(UserNotification).delete()
db.query(GuestControl).delete()
db.query(UserProfile).delete()
db.query(UserNotification).delete()
db.query(GuestControl).delete()
db.query(ProspectiveConnection).delete()
db.query(User).delete()
db.commit()



new_user = User(username="Tester1", hashed_password="ValidPass1!",
                    school="USF", first_name="Akmal", last_name="Kurbanov", premium=True)
new_user2 = User(username="Tester2", hashed_password="ValidPass1!", 
                                    school="USF", first_name="Umar", last_name="Khan", premium=False)
new_user3 = User(username="Tester3", hashed_password="ValidPass1!", 
                                    school="USF", first_name="Mukund", last_name="Sharma", premium=False)
        
db.add(new_user)
db.add(new_user2)
db.add(new_user3)
db.commit()

Tester1 = db.query(User).filter(User.username == "Tester1").first() #FIx this so this is object of UserInfo class
Tester2 = db.query(User).filter(User.username == "Tester2").first()
Tester3 = db.query(User).filter(User.username == "Tester3").first()


def test_check_password_valid():
    assert check_password("ValidPass1!") == True


def test_check_password_invalid():
    assert check_password("short") == False
    assert check_password("nocapitalletter") == False
    assert check_password("noSpecialCharacter123") == False

@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['no', 'no', 'yes', 'ValidPass1!', 'Tester4' ,'Test School', 'Test', 'User', 'yes'])
def test_signup(mock_input, mock_main_hub):
    # Call the signup function
    result = signup(db)
    assert result == "Test Completed"


@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Tester4', 'ValidPass1!'])
def test_login(mock_input, mock_main_hub):
    assert login(db) == "Successful Login"


@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Tester4', 'InvalidPassword!', "no"])
def test_login_invalid_password(mock_input, mock_main_hub):
    assert login(db) == "Not Successful Login"

@patch('builtins.input', side_effect=['no', 'no', 'yes', 'ValidPass1!', 'Tester4' ,'Test School', 'Test', 'User', 'no'])
@patch('main.signup', return_value=None)
def test_signup_with_duplicate_username(mock_input, mock_signup):
    # Attempt to sign up with a username that already exists
    result = signup(db)
    assert result == "Username already in use"


@patch('main.main_hub', return_value=None)
@patch('main.signup', return_value=None)
def test_findByFirstName (mock_main_hub, mock_signup):
    assert find_user_by_first_last_name("Akmal", "Kurbanov", db) == "Person is found"

@patch('main.main_hub', return_value=None)
@patch('main.signup', return_value=None)
def test_findByFirstName_incorrect (mock_main_hub, mock_signup):
    assert find_user_by_first_last_name("Not", "Exist", db) == "Person is not found"

@patch('main.main_hub', return_value=None) #Fix this so it properly works
@patch('builtins.input', side_effect=['XYZ'])               
def test_find_new_friends_Could_Not_Find(mock_main_hub, mock_input):
    assert find_new_friends_and_send_request(Tester1, db) == "No users found"


@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Kurbanov', Tester1.id])               
def test_find_new_friends_Could_Not_Yourself(mock_main_hub, mock_input):
    assert find_new_friends_and_send_request(Tester1, db) == "Cannot send friend request to self"


@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Kurbanov', '0'])               
def test_find_new_friends_back_to_main(mock_main_hub, mock_input):
    assert find_new_friends_and_send_request(Tester1, db) == "Return to Main Hub"

#ADD CASE FOR FRIENDSHIP ALREADY EXISTS
@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Kurbanov', 'TriggerError', 'Anything'])               
def test_find_new_friends_back_to_main_v2(mock_main_hub, mock_input):
    assert find_new_friends_and_send_request(Tester1, db) == "Return to Main Hub 2"


@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Khan', Tester2.id]) 
def test_find_new_friends_back_to_main_v3(mock_main_hub, mock_input):
    assert find_new_friends_and_send_request(Tester1, db) == "Successfully sent friend request."

@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['Khan', Tester2.id]) 
def test_send_friend_request(mock_input, mock_main_hub):
    assert find_new_friends_and_send_request(Tester1, db) == "Friend request already sent"

@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=["Kurbanov", Tester1.id])
def test_pending_friend_request_exists(mock_main_hub, mock_input):
    assert find_new_friends_and_send_request(Tester2, db) == "Pending friend request exists"



if __name__ == "__main__":
        # Run the tests
        pytest.main(["-s"])
