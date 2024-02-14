import pytest
from sqlalchemy.orm import Session
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
    db
)

# Fixture for initializing a test database session
@pytest.fixture(scope="module")
def test_db_session():
    yield next(db)


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
