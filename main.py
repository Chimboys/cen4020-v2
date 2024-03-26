import re
import hashlib
from user import UserCreate, UserInfo, Friends
# Importing the job_actions function from jobs_func.py
from jobs_func import job_actions
import models
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError


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


def find_user_by_first_last_name(first_name: str, last_name: str, db: Session):
    if db.query(models.User).filter(and_(models.User.first_name == first_name, models.User.last_name == last_name)).first():
        print("Person is a part of the InCollege system")
        signup(db)
    else:
        print("They are not a part of the InCollege system")
        print("Goodbye")


def handle_useful_links_choice(userData, db, choice):
    if choice == 1:
        handle_general_links(userData)
    elif choice in (2, 3, 4):
        print("Under construction for Browse InCollege, Business Solutions, Directories")
    else:
        print("Invalid choice")


def handle_general_links(userData):
    print("General Links:")
    print("1. Sign Up")
    print("2. Help Center")
    print("3. About")
    print("4. Press")
    print("5. Blog")
    print("6. Careers")
    print("7. Developers")
    print("0. Main Hub")

    sub_choice = input("Enter your choice: ")

    if sub_choice == '1':
        signup(db)
    elif sub_choice == '2':
        print("We're here to help")
    elif sub_choice == '3':
        print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
    elif sub_choice == '4':
        print("In College Pressroom: Stay on top of the latest news, updates, and reports")
    elif sub_choice in ('5', '6', '7'):
        print("Under construction")
    elif sub_choice == '0':
        main_hub(userData, db)
    else:
        print("Invalid choice")


def handle_guest_controls(userData, db):
    print("Guest Controls:")
    val = db.query(models.GuestControl).filter(
        models.GuestControl.user_id == userData.id).first()
    print("Select the guest control you would like to see:")
    print("1. InCollege Email", val.incollege_email_enabled)
    print("2. SMS", val.sms_enabled)
    print("3. Targeted Advertising", val.targeted_advertising_enabled)
    print("0. Exit")

    while True:
        print("Which one would you like to change?")
        choice = input("Enter your choice: ")
        if choice == '1':
            val.incollege_email_enabled = not val.incollege_email_enabled
            db.commit()
        elif choice == '2':
            val.sms_enabled = not val.sms_enabled
            db.commit()
        elif choice == '3':
            val.targeted_advertising_enabled = not val.targeted_advertising_enabled
            db.commit()
        elif choice == '0':
            main_hub(userData, db)
        else:
            print("Invalid choice")


def handle_important_links_choice(userData, db, choice):
    # Implement logic for handling each important link based on the choice
    if choice == 5:
        if userData:
            print("1. Guest Controls")
            print("0. Exit")
            sub_choice = input("Enter your choice: ")
            if sub_choice == '1':
                handle_guest_controls(userData, db)
            elif sub_choice == '0':
                main_hub(userData, db)
            else:
                print("Invalid choice")
        else:
            print("Log in to access Guest Controls")
    elif choice == 1:
        print("Copyright (c) [Year] [Full Name]", "All rights reserved.",
              "This software, InCollege, is the property of Team Beige. Any redistribution, modification, or reproduction is not permitted without the express consent of team Beige.", end="\n")

    elif choice == 2:
        print("InCollege is a dedicated platform designed to empower college students in their job search by providing a space exclusively for them and potential employers. Join InCollege today and take a step towards shaping your professional future.")

    elif choice == 3:
        print("Empowering inclusive education: Our inCollege app is designed with accessibility in mind, ensuring a seamless and enriching experience for users of all abilities.")

    elif choice == 4:
        print("""
User Agreement

This User Agreement ("Agreement") is a contract between you and InCollege and applies to your use of InCollege services.

1. Acceptance of Terms

By using InCollege, you agree to this Agreement and any other rules or policies that we may publish from time to time.

2. Eligibility and Content

You must be at least 18 years old to use [App Name]. You are responsible for all content posted and activity that occurs under your account.

InCollege
USF Computer Science Department
""")

    elif choice == 6:
        print("InCollege app uses essential, analytics, and functionality cookies to enhance your experience, remembering preferences and analyzing usage patterns; by using the app, you consent to the use of cookies as outlined in our Cookie Policy.")

    elif choice == 7:
        print("""
        Copyright (c) 2024 InCollege

        All rights reserved.

        This software, [App Name], is the property of InCollege. Any redistribution, modification, or reproduction is not permitted without the express consent of InCollege.
        """)

    elif choice == 8:
        print("InCollege app is committed to fostering inclusive education, providing a seamless and enriching experience for users of all abilities, promoting diversity, and ensuring a safe and supportive learning environment.")

    elif choice == 9:
        print("1. Language Preference")
        print("0. Exit")
        sub_choice = input("Enter your choice: ")
        if sub_choice == '1':
            if userData:
                handle_language_preference(userData, db)
            else:
                print("Log in to access Language Preference")
        elif sub_choice == '0':
            main_hub(userData, db)
        else:
            print("Invalid choice")

    else:
        print("Invalid choice")


def handle_language_preference(userData, db):
    print("Language Controls:")
    val = db.query(models.GuestControl).filter(
        models.GuestControl.user_id == userData.id).first()
    print("Select an option:")
    print("1. Language preference", val.language_preference)
    print("0. Exit")

    while True:
        print("Would you like to change your preference?")
        choice = input("Enter your choice: ")
        if choice == 'Yes':
            print("Choose which language you would like to use")
            print("1. English")
            print("2. Spanish")
            sub_choice = input("Enter your choice: ")
            if sub_choice == '1':
                val.language_preference = "English"
                db.commit()
            elif sub_choice == '2':
                val.language_preference = "Spanish"
                db.commit()
            else:
                print("Invalid choice")
        elif choice == 'No':
            main_hub(userData, db)
        else:
            print("Invalid choice")


def find_user_by_first_last_name_login(first_name: str, last_name: str, userData: UserInfo, db: Session):
    if db.query(models.User).filter(and_(models.User.first_name == first_name, models.User.last_name == last_name)).first():
        print("Person is a part of the InCollege system")

        signup(db)
    else:
        print("They are not a part of the InCollege system")
        new_prospective_connection = models.ProspectiveConnection(
            caller_id=userData.id, first_name=first_name, last_name=last_name)
        db.add(new_prospective_connection)
        db.commit()
        main_hub(userData, db)
        print("Goodbye")


def signup(db):
    # Get user input
    print("Sarah, a determined college student majoring in marketing, faced challenges in finding internships and entry-level positions that aligned with her goals. However, her journey took a positive turn when she discovered InCollege, a specialized job search website for college students. This platform provided curated job listings, networking opportunities, and time-saving tools tailored to Sarah's needs. With InCollege's support, Sarah secured a dream internship at a tech startup, built a strong professional network, and experienced both academic and professional growth. Ultimately, Sarah's success story highlights how leveraging specialized resources can empower college students to kickstart their careers and achieve their goals", "\n")

    print("Welcome to InCollege: Where you can find your dream job, make new friends, and learn new skills.", "\n")
    ans = input("Would you like to view success video? (yes/no): ")
    if ans.lower() == 'yes':
        print("Video playing at https://www.youtube.com/watch?v=dQw4w9WgXcQ", "\n")

    has_account = input("Do you already have an account? (yes/no): ")
    if has_account.lower() == 'yes':
        login(db)
        return
    choice = str(input("Would you like to sign up? (yes/no): "))
    if choice.lower() == 'no':
        choiceFind = str(
            input("Would you like to find a user by first and last name? (yes/no): "))
        if choiceFind.lower() == 'yes':
            first_name = input("Enter the first name of the user: ")
            last_name = input("Enter the last name of the user: ")
            find_user_by_first_last_name(first_name, last_name, db)
            return
        else:
            print("Goodbye")
            return

    hashed_password = input("Enter your password: ")

    # Check password
    if check_password(hashed_password):
        # Checking amount of users
        username = input("Enter your username: ")
        school = input("Enter your school: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        if db.query(func.count(models.User.id)).scalar() > 10:
            print("You have reached the maximum number of users.")
            continue_signup = input(
                "Would you like to login instead? (yes/no)")
            if continue_signup.lower() == 'yes':
                login(db)
            return
        if db.query(models.User).filter(models.User.username == username).first():
            print("Username already in use.")
            continue_signup = input(
                "Would you like to login instead? (yes/no)")  # change
            if continue_signup.lower() == 'yes':
                login(db)
            return
        else:
            print("Not duplicate")
        user_create = UserCreate(username=username, hashed_password=hashed_password,
                                 school=school, first_name=first_name, last_name=last_name)
        new_user = models.User(**user_create.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = UserInfo(id=new_user.id, username=new_user.username, school=new_user.school,
                        first_name=new_user.first_name, last_name=new_user.last_name)
        default_guest_control = models.GuestControl(
            incollege_email_enabled=True,
            sms_enabled=True,
            targeted_advertising_enabled=True,
            user_id=new_user.id
        )
        db.add(default_guest_control)
        db.commit()

        new_user.guest_control = default_guest_control
        db.commit()

        # remainder = db.query(models.ProspectiveConnection).filter(models.ProspectiveConnection.first_name == first_name, models.ProspectiveConnection.last_name == last_name).first()
        # if remainder:
        #     caller = db.query(models.User).filter(models.User.id == remainder.caller_id).first()
        #     print(f"Hi, {caller.first_name} {caller.last_name} was looking for you")
        #     friend = Friends(user_id=caller.id, friend_id=new_user.id)
        #     friendship = models.Friendship(**friend.dict())
        #     db.add(friendship)
        #     db.delete(remainder)
        #     db.commit()

        main_hub(user, db)

    else:

        continue_signup = input(
            "Password is invalid. Do you want to continue signup? (yes/no): ")
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
        continue_signup = input(
            "Password is invalid. Do you want to continue login? (yes/no): ")
        if continue_signup.lower() == 'yes':
            login(db)
        else:
            print("Login cancelled.")
        return

    queryUser = db.query(models.User).filter(
        models.User.username == username).first()
    if queryUser is None:
        print("Sigh Up first")
        return
    elif queryUser.hashed_password != password:
        print("Password is incorrect")
        return
    print("Login successfuly")
    user = UserInfo(id=queryUser.id, username=queryUser.username, school=queryUser.school,
                    first_name=queryUser.first_name, last_name=queryUser.last_name)

    main_hub(user, db)


def logout(userData, db):
    print("Logout successful")
    return None, None  # Returning None for userData and db


def main_hub(userData: UserInfo = None, db=None):

    while True:
        print("Welcome to InCollege!")

        # Provide initial choice for the user
        print("Select Links to Explore:")
        print("1. Useful Links")
        print("2. Important Links")
        print("3. User Actions")
        if userData:
            print("4. Job search and Internships")
        print("5. Exit")
        initial_choice = input("Enter your choice: ").lower()

        if initial_choice == '5':
            print("Goodbye")
            break
        elif initial_choice == '1':
            explore_links(userData, db, "Useful Links")
        elif initial_choice == '2':
            explore_links(userData, db, "Important Links")
        elif initial_choice == '3':
            userData, db = user_actions(userData, db)
        elif initial_choice == '4':
            job_actions(userData, db)
        else:
            print("Invalid choice")


def explore_links(userData, db, link_type):
    while True:
        if userData:
            print(f"Welcome, {userData.first_name}!")
        else:
            print("Welcome! (You are not logged in)")

        print(f"{link_type}:")
        if link_type == "Useful Links":
            print("1. General")
            print("2. Browse InCollege")
            print("3. Business Solutions")
            print("4. Directories")
        elif link_type == "Important Links":
            print("1. Copyright Notice")
            print("2. About")
            print("3. Accessibility")
            print("4. User Agreement")
            print("5. Privacy Policy")
            print("6. Cookie Policy")
            print("7. Copyright Policy")
            print("8. Brand Policy")
            print("9. Languages")
        else:
            print("Invalid link type")

        print("0. Go back to main hub")
        choice = input("Enter your choice: ")

        if choice == '0':
            break
        elif link_type == "Useful Links" and choice in ('1', '2', '3', '4'):
            handle_useful_links_choice(userData, db, int(choice))
        elif link_type == "Important Links" and choice in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
            handle_important_links_choice(userData, db, int(choice))
        else:
            print("Invalid choice")


def user_actions(userData, db):
    while True:
        if userData:
            print(f"Welcome, {userData.first_name}!")
            print("User Actions:")
            print("1. Search for a job")
            print("2. Find new friends")
            print("3. Learn new skills")
            print("4. View all friends")
            print("5. Handle Friend Requests")
            print("6. Logout")
            print("7. Create/Update User Profile")
            print("0. Exit")
            user_choice = input("Enter your choice: ").lower()

            if user_choice == '1':
                job_actions(userData, db)

                pass
            elif user_choice == '2':
                find_new_friends_and_send_request(userData, db)
            elif user_choice == '3':
                learn_new_skills(userData, db)
            elif user_choice == '4':
                view_all_friends(userData, db)
                disconnect_choice = input(
                    "Do you want to disconnect from a friend? (yes/no): ")
                if disconnect_choice.lower() == 'yes':
                    friend_id_to_disconnect = int(
                        input("Enter the User ID of the friend you want to disconnect from: "))
                    disconnect_from_friend(
                        userData.id, friend_id_to_disconnect, db)
            elif user_choice == '5':
                handle_friend_requests(userData, db)
            elif user_choice == '6':
                userData, db = logout(userData, db)
                if userData is None and db is None:
                    break
            elif user_choice == '7':
                create_profile(db, userData.id)
            elif user_choice == '0':
                print("Goodbye")
                break
            else:
                print("Invalid choice")
        else:
            print("You need to log in to perform user actions.")
            signup(db)

    return userData, db


# Fix it so it does not comeback to the main hub once user does not have friends
def view_all_friends(userData: UserInfo, db):

    friends = db.query(models.Friendship).filter(or_(models.Friendship.user_id == userData.id,
                                                     models.Friendship.friend_id == userData.id)).all()

    if not friends:
        print("You have no friends")
        main_hub(userData, db)
        return

    for index in friends:

        friend = db.query(models.User).filter(
            models.User.id == (index.friend_id)).first()
        if friend.id == userData.id:

            friend = db.query(models.User).filter(
                models.User.id == (index.user_id)).first()

        else:
            friend = db.query(models.User).filter(
                models.User.id == (index.friend_id)).first()

        print(
            f'First name: {friend.first_name}, last name: {friend.last_name}, school: {friend.school}, id: {friend.id}')
    choice = input("Would you like to go back to the main hub? (yes/no): ")
    if choice.lower() == 'yes':
        main_hub(userData, db)
    else:
        print("Goodbye")
        return


def disconnect_from_friend(user_id: int, friend_id: int, db: Session):
    friendship = db.query(models.Friendship).filter(
        ((models.Friendship.user_id == user_id) & (models.Friendship.friend_id == friend_id)) |
        ((models.Friendship.user_id == friend_id) &
         (models.Friendship.friend_id == user_id))
    ).first()

    if friendship:
        db.delete(friendship)
        db.commit()
        print("Successfully disconnected from the friend.")
    else:
        print("Friendship not found.")


def find_new_friends_and_send_request(userData: UserInfo, db):
    last_name_to_search = input("Enter the last name to search: ")
    matching_users = db.query(models.User).filter(
        models.User.last_name == last_name_to_search).all()

    if not matching_users:
        print(f"No users found with the last name '{last_name_to_search}'.")
        main_hub(userData, db)
        return

    print("Matching Users:")
    for user in matching_users:
        print(
            f"User ID: {user.id}, First Name: {user.first_name}, Last Name: {user.last_name}, School: {user.school}")

    user_id_to_add = input(
        "Enter the User ID you want to send a friend request to (or enter '0' to go back to the main hub): ")

    if user_id_to_add == '0':
        main_hub(userData, db)
        return

    try:
        user_id_to_add = int(user_id_to_add)
        if user_id_to_add == userData.id:
            print("You cannot send a friend request to yourself.")
        elif db.query(models.Friendship).filter(or_(
                and_(models.Friendship.user_id == userData.id,
                     models.Friendship.friend_id == user_id_to_add),
                and_(models.Friendship.user_id == user_id_to_add, models.Friendship.friend_id == userData.id))).first():
            print("Friendship already exists.")
        else:
            send_friend_request(userData.id, user_id_to_add, db)
    except ValueError:
        print("Invalid User ID. Please enter a valid numeric User ID.")

    main_hub(userData, db)


def send_friend_request(caller_id, receiver_id, db):
    new_prospective_connection = models.ProspectiveConnection(
        caller_id=caller_id, receiver_id=receiver_id)
    db.add(new_prospective_connection)
    db.commit()
    print("Friend request sent successfully.")


def handle_friend_requests(userData: UserInfo, db):
    while True:
        print("Friend Request Handling:")
        print("1. View and Accept Friend Requests")
        print("2. Go back to user actions")
        choice = input("Enter your choice: ")

        if choice == '1':
            accept_or_reject_friend_requests(userData, db)
        elif choice == '2':
            break
        else:
            print("Invalid choice")


def accept_or_reject_friend_requests(userData: UserInfo, db):
    pending_requests = db.query(models.ProspectiveConnection).filter(
        models.ProspectiveConnection.receiver_id == userData.id).all()

    if not pending_requests:
        print("No pending friend requests.")
        return

    print("Pending Friend Requests:")
    for request in pending_requests:
        caller = db.query(models.User).filter(
            models.User.id == request.caller_id).first()
        print(
            f"User ID: {caller.id}, First Name: {caller.first_name}, Last Name: {caller.last_name}, School: {caller.school}")

    user_id_to_accept_or_reject = input(
        "Enter the User ID you want to accept or reject as a friend (or enter '0' to cancel): ")

    if user_id_to_accept_or_reject == '0':
        return

    try:
        user_id_to_accept_or_reject = int(user_id_to_accept_or_reject)
        prospective_connection = db.query(models.ProspectiveConnection).filter(
            and_(models.ProspectiveConnection.caller_id == user_id_to_accept_or_reject, models.ProspectiveConnection.receiver_id == userData.id)).first()
        if prospective_connection:
            print("1. Accept friend request")
            print("2. Reject friend request")
            choice = input("Do you want to accept or reject: ")

            if choice == 1:
                friend = Friends(
                    user_id=user_id_to_accept_or_reject, friend_id=userData.id)
                friendship = models.Friendship(**friend.dict())
                db.add(friendship)
                db.delete(prospective_connection)
                db.commit()
                print("Friend request accepted successfully.")
            else:
                db.delete(prospective_connection)
                db.commit()
                print("Friend request rejected successfully")
        else:
            print(
                "Invalid User ID. No pending friend request found for the specified user.")
    except ValueError:
        print("Invalid User ID. Please enter a valid numeric User ID.")


def create_profile(db, userData):
    # Check if the user already has a profile
    existing_profile = db.query(models.UserProfile).filter_by(
        user_id=userData.id).first()
    if existing_profile:
        print("You already have a profile. Would you like to update it?")
        update_profile_option = input(
            "Enter 'yes' to update or 'no' to exit: ").lower()
        if update_profile_option == 'yes':
            edit_profile_sections(db, userData, existing_profile)
        else:
            print("Exiting profile creation.")
            main_hub(userData, db)
        return

    # Create UserProfile object with default values
    profile = models.UserProfile(
        title="N/A",
        major="N/A",
        university_name="N/A",
        about_student="N/A",
        experience=[],
        education=[],
        user=userData
    )
    db.add(profile)
    db.commit()

    print("Profile creation successful!")
    edit_profile_sections(db, userData, profile)


def edit_profile_sections(db, userData, profile):
    while True:
        print("What part of your profile would you like to update?")
        print("1. Title")
        print("2. Major")
        print("3. University Name")
        print("4. About")
        print("5. Experience")
        print("6. Education")
        print("0. Exit")

        option = input(
            "Enter the number corresponding to the part you want to update: ")

        if option == '1':
            profile.title = input("Enter a new title: ")
        elif option == '2':
            profile.major = input("Enter your major: ").title()
        elif option == '3':
            profile.university_name = input(
                "Enter your university name: ").title()
        elif option == '4':
            profile.about_student = input("Enter information about yourself: ")
        elif option == '5':
            edit_experience(db, userData)
        elif option == '6':
            edit_education(db, userData)
        elif option == '0':
            db.commit()
            print("Profile updated successfully!")
            main_hub(userData, db)  # Redirect to main hub
            break
        else:
            print("Invalid option. Please enter a number between 0 and 6.")


def edit_experience(db, userData):
    # Fetch the user's existing profile
    existing_profile = db.query(models.UserProfile).filter_by(
        user_id=userData.id).first()
    if not existing_profile:
        print("User profile not found.")
        return

    # Display the current experience information
    print("Current Experience Information:")
    for i, experience in enumerate(existing_profile.experiences, start=1):
        print(f"Experience {i}:")
        print(f"Title: {experience.title}")
        print(f"Employer: {experience.employer}")
        print(f"Date Started: {experience.date_started}")
        print(f"Date Ended: {experience.date_ended}")
        print(f"Location: {experience.location}")
        print(f"Description: {experience.description}")
        print()

    # Prompt the user to select an experience to edit
    experience_index = int(
        input("Enter the index of the experience you want to edit (or 0 to cancel): "))
    if experience_index == 0:
        return

    if experience_index < 1 or experience_index > len(existing_profile.experiences):
        print("Invalid experience index.")
        return

    # Select the experience to edit
    experience_to_edit = existing_profile.experiences[experience_index - 1]

    # Prompt the user to enter new experience information
    print("Enter new experience information:")
    title = input("Title: ")
    employer = input("Employer: ")
    date_started = input("Date Started: ")
    date_ended = input("Date Ended: ")
    location = input("Location: ")
    description = input("Description: ")

    # Update the experience information
    experience_to_edit.title = title
    experience_to_edit.employer = employer
    experience_to_edit.date_started = date_started
    experience_to_edit.date_ended = date_ended
    experience_to_edit.location = location
    experience_to_edit.description = description

    # Commit the changes to the database
    db.commit()
    print("Experience information updated successfully.")


def edit_education(db, userData):
    # Fetch the user's existing profile
    existing_profile = db.query(models.UserProfile).filter_by(
        user_id=userData.id).first()
    if not existing_profile:
        print("User profile not found.")
        return

    # Display the current education information
    print("Current Education Information:")
    print(f"School: {existing_profile.school}")
    print(f"Degree: {existing_profile.degree}")
    print(f"Years Attended: {existing_profile.years_attended}")
    print()

    # Prompt the user to enter new education information
    print("Enter new education information:")
    school = input("School: ")
    degree = input("Degree: ")
    years_attended = input("Years Attended: ")

    # Update the education information
    existing_profile.school = school
    existing_profile.degree = degree
    existing_profile.years_attended = years_attended

    # Commit the changes to the database
    db.commit()
    print("Education information updated successfully.")


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
    main_hub(db=db)
finally:
    db.close()
