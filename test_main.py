import pytest
from unittest.mock import patch

from sqlalchemy.orm import Session
import sqlalchemy
from main import (
    check_password,
    find_user_by_first_last_name,
    find_user_by_first_last_name_login,
    signup,
    login,
    post_a_job,
    main_hub,
    view_all_friends,
    find_new_friends,
    add_friends,
    learn_new_skills,
    db,
    User, 
    UserCreate
)

# Fixture for initializing a test database session
@pytest.fixture(scope="module")
def test_db_session():
    yield next(db)


def populate_db():
    db = test_db_session()
    # Assuming the database is empty
    new_user = User(username="Tester1", hashed_password="ValidPassword1!", email="test1@gmail.com",
                school="USF", first_name="Akmal", last_name="Kurbanov", premium=False)
    new_user2 = User(username="Tester2", hashed_password="ValidPassword1!", email="test2@gmail.com",
                                 school="USF", first_name="Umar", last_name="Khan", premium=False)
    new_user3 = User(username="Tester3", hashed_password="ValidPassword1!", email="test3@gmail.com",
                                 school="USF", first_name="Mukund", last_name="Mukund Sharma", premium=False)
    
    db.add(new_user)
    db.add(new_user2)
    db.add(new_user3)
    db.commit()

    
def clear_db():
    db = test_db_session()
    db.query(User).delete()
    db.commit()


@patch('builtins.input', side_effect=['no', 'no', 'yes', 'ValidPassword1', 'Tester4' ,'Test School', 'Test', 'User'])
def test_signup(mock_input, test_db_session):
    # Call the signup function
    result = signup(test_db_session)
    assert result == "Test Completed"


   
    
                  

def test_check_password_valid():
    assert check_password("ValidPassword1!") == True


def test_check_password_invalid():
    assert check_password("short") == False
    assert check_password("nocapitalletter") == False
    assert check_password("noSpecialCharacter123") == False


def test_find_user_by_first_last_name_exists(test_db_session):
    # Assuming there's a user with the given first and last name in the test database
    assert find_user_by_first_last_name("John", "Doe", test_db_session) == True


def test_find_user_by_first_last_name_not_exists(test_db_session):
    # Assuming there's no user with the given first and last name in the test database
    assert find_user_by_first_last_name("Nonexistent", "User", test_db_session) == False

if __name__ == "__main__":
    pytest.main(["-v", "-s", "--tb=no", __file__])
