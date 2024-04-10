import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session

from main import (
    get_notification, 
    create_job_post, 
    delete_job_post, 
    register_new_student,
    get_jobs_applied_count,
)
from database import User, JobApplication, session, get_db

# Fixture for initializing a test database session
@pytest.fixture(scope="module")
def test_db_session():
    db = next(get_db())
    yield db

# Test for job application reminder notification
@patch('main.get_notification')
def test_job_application_reminder(mock_get_notification, test_db_session):
    user_id = 1  # Assuming user_id 1 exists for testing
    mock_get_notification.return_value = "Remember you're going to want to have a job when you graduate."
    notification = get_notification(user_id, test_db_session)
    assert "Remember – you're going to want to have a job when you graduate." in notification

# Test for profile creation reminder notification
@patch('main.get_notification')
def test_profile_creation_reminder(mock_get_notification, test_db_session):
    user_id = 2  # Assuming user_id 2 exists for testing
    mock_get_notification.return_value = "Don't forget to create a profile"
    notification = get_notification(user_id, test_db_session)
    assert "Don't forget to create a profile" in notification

# Test for unread messages notification
@patch('main.get_notification')
def test_unread_messages_notification(mock_get_notification, test_db_session):
    user_id = 3  # Assuming user_id 3 exists for testing
    mock_get_notification.return_value = "You have messages waiting for you"
    notification = get_notification(user_id, test_db_session)
    assert "You have messages waiting for you" in notification

# Test for job application count notification
@patch('main.get_notification')
@patch('main.get_jobs_applied_count')
def test_jobs_applied_notification(mock_get_jobs_applied_count, mock_get_notification, test_db_session):
    user_id = 4  # Assuming user_id 4 exists for testing
    mock_get_jobs_applied_count.return_value = 5
    mock_get_notification.return_value = "You have currently applied for 5 jobs"
    notification = get_notification(user_id, test_db_session)
    assert "You have currently applied for 5 jobs" in notification

# Test for new job posting notification
@patch('main.get_notification')
def test_new_job_posted_notification(mock_get_notification, test_db_session):
    user_id = 5  # Assuming user_id 5 exists for testing
    mock_get_notification.return_value = "A new job Test Job has been posted"
    notification = get_notification(user_id, test_db_session)
    assert "A new job Test Job has been posted" in notification

# Test for deleted job notification
@patch('main.get_notification')
def test_deleted_job_notification(mock_get_notification, test_db_session):
    user_id = 6  # Assuming user_id 6 exists for testing
    mock_get_notification.return_value = "A job that you applied for Old Job has been deleted"
    notification = get_notification(user_id, test_db_session)
    assert "A job that you applied for Old Job has been deleted" in notification

# Test for new student joined notification
@patch('main.get_notification')
def test_new_student_joined_notification(mock_get_notification, test_db_session):
    user_id = 7  # Assuming user_id 7 exists for testing
    new_user_first_name = "John"
    new_user_last_name = "Doe"
    mock_get_notification.return_value = f"{new_user_first_name} {new_user_last_name} has joined InCollege"
    notification = get_notification(user_id, test_db_session)
    assert f"{new_user_first_name} {new_user_last_name} has joined InCollege" in notification

if _name_ == "_main_":
    pytest.main(["-s"])