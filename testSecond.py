import pytest
from unittest.mock import patch


from user import UserCreate, UserInfo, Friends
# Importing the job_actions function from jobs_func.py
from jobs_func import job_actions
from models import User, GuestControl
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import sqlalchemy
from database import get_db

from main import (
    check_password,
    signup,
    learn_new_skills,
)

db = next(get_db())

# Fixture for initializing a test database session
@pytest.fixture(scope="module")
def test_db_session():
    # setup code here
    db = next(get_db())
    yield db
    # teardown code here




def populate_db():
    # Assuming the database is empty

    new_user = User(username="Tester1", hashed_password="ValidPass1!",
                school="USF", first_name="Akmal", last_name="Kurbanov", premium=False)
    new_user2 = User(username="Tester2", hashed_password="ValidPass1!", 
                                 school="USF", first_name="Umar", last_name="Khan", premium=False)
    new_user3 = User(username="Tester3", hashed_password="ValidPass1!", 
                                 school="USF", first_name="Mukund", last_name="Mukund Sharma", premium=False)
    
    db.add(new_user)
    db.add(new_user2)
    db.add(new_user3)
    db.commit()

    
def clear_db():
    db.query(GuestControl).delete()
    db.query(User).delete()
    db.commit()




@patch('main.main_hub', return_value=None)
@patch('builtins.input', side_effect=['no', 'no', 'yes', 'ValidPass1!', 'Tester4' ,'Test School', 'Test', 'User'])
def test_signup(mock_input, mock_main_hub):
    # Call the signup function
    clear_db()
    populate_db()

    result = signup(db)
    assert result == "Test Completed"


   
    
                
def test_check_password_valid():
    assert check_password("ValidPass1!") == True


def test_check_password_invalid():
    assert check_password("short") == False
    assert check_password("nocapitalletter") == False
    assert check_password("noSpecialCharacter123") == False


if __name__ == "__main__":
        # Run the tests
        pytest.main(["-s"])
