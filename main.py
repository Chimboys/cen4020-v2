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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from profiles import Profile
import hashlib


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
        return "Person is found"
    else:
        print("They are not a part of the InCollege system")
        print("Goodbye")
        return "Person is not found"


def handle_useful_links_choice(userData, db, choice):
    if choice == 1:
        handle_general_links(userData)
    elif choice in (2, 3, 4):
        print("Under construction for Browse InCollege, Business Solutions, Directories")
    else:
        print("Invalid choice")


def inbox(userData, db):
    messages = db.query(models.Message).filter(
        models.Message.receiver_id == userData.id).all()
    if messages == None:
        print("You Do Not Have Any Messages")
        print()
        message_handler(userData, db)
    newMessages = []
    readMessages = []
    idMessages = []
    for message in messages:
        if message.read == True:
            readMessages.append(message)
        else:
            newMessages.append(message)
        idMessages.append(message.id)

    print()
    print("New Messages")
    if len(newMessages) == 0:
        print("You do not have new messages")
    else:
        for message in newMessages:
            sender = db.query(models.User).filter(
                models.User.id == message.sender_id).first()
            print(
                f"ID OF MESSAGE: {message.id}, From: {sender.first_name} {sender.last_name} with ID: {message.sender_id}, Sent at: {message.sent_at}")

    print()
    print("Read Messages")
    if len(readMessages) == 0:
        print("You do not have new messages")
    else:
        for message in readMessages:
            sender = db.query(models.User).filter(
                models.User.id == message.sender_id).first()
            print(
                f"ID OF MESSAGE: {message.id}, From: {sender.username} with ID: {message.sender_id}, Sent at: {message.sent_at}")
    print()
    if len(newMessages) == 0 and len(readMessages) == 0:
        print()
        message_handler(userData, db)

    print("Would you like to read any of the messages? ( 'yes' to continue)")
    choice = input("Enter your choice: ")
    if choice.lower() == "yes":
        while True:
            try:
                messageChoice = int(
                    input("Enter message ID or type 'quit' to go to main hub: "))
                if messageChoice in idMessages:
                    print()
                    read_message(messageChoice, userData, db)
                    pass
                else:
                    print("The message does not exist. Please re-enter ID.")
            except ValueError:
                if messageChoice.lower() == 'quit':
                    main_hub(userData, db)
                    break
                else:
                    print(
                        "Invalid input. Please enter a valid ID or type 'quit' to go to main hub.")
    else:
        print()
        message_handler(userData, db)


def read_message(message_id, userData, db):
    message = db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.receiver_id == userData.id).first()

    sender = db.query(models.User).filter(
        models.User.id == message.sender_id).first()
    print(f"From: {sender.username}, Sent at: {message.sent_at}")
    print(f"{message.content}")
    print()

    db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.receiver_id == userData.id
    ).update({models.Message.read: True}, synchronize_session=False)
    db.commit()

    # set read to true message.update !!!
    while True:
        print("Would you like to reply, delete, or read other messages? ")
        choice = input().lower()

        if choice == 'read':
            inbox(userData, db)
        elif choice == 'reply':
            print()
            send_message(userData, sender.id, db)
        elif choice == 'delete':
            delete_message(userData, message_id, db)
        else:
            print("Invalid input. Would you like to continue? (Type 'yes' to continue or 'no' to go back to main_hub)")
            main_choice = input().lower()
            if main_choice == "yes":
                continue
            elif main_choice == "no":
                main_hub(userData, db)
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")


def delete_message(userData, message_id, db):
    message = db.query(models.Message).filter(
        models.Message.id == message_id).first()
    db.delete(message)
    db.commit()
    print("Message deleted successfully")
    print()
    message_handler(userData, db)


def send_message(userData, receiver_id, db):
    if receiver_id == userData.id:
        print("You cannot send a message to yourself")
        print()
        message_handler(userData, db)
    message = input("Enter your message: ")
    new_message = models.Message(
        sender_id=userData.id, receiver_id=receiver_id, content=message)
    db.add(new_message)
    db.commit()
    print("Message sent successfully")
    print()
    message_handler(userData, db)


def upgrade_to_premium(userData, db):
    print("You are about to upgrade to a plus user with a monthly fee of $10. Would you like to continue? (yes/no)")
    choice = input()
    if choice.lower() == 'no':
        print("You have chosen not to upgrade to a premium user")
        print()
        message_handler(userData, db)
    elif choice.lower() == 'yes':
        one_month_from_now = datetime.now() + relativedelta(months=1)
        db.query(models.User).filter(models.User.id == userData.id).update(
            {models.User.premium: True,  models.User.premium_until: one_month_from_now}, synchronize_session=False)
        db.commit()
        userData = db.query(models.User).filter(
            models.User.id == userData.id).first()
        print("You are now a premium user")
        message_handler(userData, db)


def message_handler(userData, db):
    print("Messages:")
    print("1. View inbox")
    print("2. Send message")
    if userData.premium == False:
        print("3. Update to Plus")  # improve update to premium !
    print("0. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        inbox(userData, db)

    elif choice == '2':
        users = db.query(models.User).all()
        print("Users:")
        allUsers = []
        for user in users:
            print(
                f"ID: {user.id}, Username: {user.username}, First Name: {user.first_name}, Last Name: {user.last_name}")
            allUsers.append(user.id)
        print()
        message_receiver = input(
            "Choose to a person to send a message to via typing his/her ID: ")
        if int(message_receiver) == userData.id:
            print("You cannot send a message to yourself")
            print()
            message_handler(userData, db)

        if int(message_receiver) not in allUsers:
            print("The user does not exist")
            print()
            message_handler(userData, db)

        if userData.premium == False:
            friends = db.query(models.Friendship).filter(or_(models.Friendship.user_id == userData.id,
                                                             models.Friendship.friend_id == userData.id)).all()

            if friends is None:
                print(
                    "You need to have friends to send a message without being a plus user")
                print()
                message_handler(userData, db)
            list_of_friends = []

            for friend in friends:
                list_of_friends.append(friend.friend_id)
                list_of_friends.append(friend.user_id)

            if int(message_receiver) not in list_of_friends:
                print("I'm sorry, you are not friends with that person")
                print()
                message_handler(userData, db)
            else:
                send_message(userData, message_receiver, db)
        elif userData.premium == True:
            send_message(userData, message_receiver, db)

    elif choice == '3' and userData.premium == False:
        upgrade_to_premium(userData, db)  # improve update to premium !

    elif choice == '0':
        print()
        main_hub(userData, db)


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
        print()
    elif sub_choice == '2':
        print("We're here to help")
        print()
    elif sub_choice == '3':
        print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
    elif sub_choice == '4':
        print("In College Pressroom: Stay on top of the latest news, updates, and reports")
        print()
    elif sub_choice in ('5', '6', '7'):
        print("Under construction")
        print()
    elif sub_choice == '0':
        main_hub(userData, db)
        print()
    else:
        print("Invalid choice")
        print()


def handle_guest_controls(userData, db):
    print("Guest Controls:")
    val = db.query(models.GuestControl).filter(
        models.GuestControl.user_id == userData.id).first()
    if val is None:
        # Create a new GuestControl record with default values
        val = models.GuestControl(user_id=userData.id, incollege_email_enabled=True,
                                  sms_enabled=True, targeted_advertising_enabled=True)
        db.add(val)
        db.commit()
    print("Select the guest control you would like to see:")
    print("1. InCollege Email", val.incollege_email_enabled)
    print("2. SMS", val.sms_enabled)
    print("3. Targeted Advertising", val.targeted_advertising_enabled)
    print("0. Exit")
    print()

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
            print()


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
            print()
    elif choice == 1:
        print("Copyright (c) 2024 Team Beige", "All rights reserved.",
              "This software, InCollege, is the property of Team Beige. Any redistribution, modification, or reproduction is not permitted without the express consent of team Beige.", end="\n")

    elif choice == 2:
        print("InCollege is a dedicated platform designed to empower college students in their job search by providing a space exclusively for them and potential employers. Join InCollege today and take a step towards shaping your professional future.")
        print()

    elif choice == 3:
        print("Empowering inclusive education: Our inCollege app is designed with accessibility in mind, ensuring a seamless and enriching experience for users of all abilities.")
        print()

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
        print()

    elif choice == 6:
        print("InCollege app uses essential, analytics, and functionality cookies to enhance your experience, remembering preferences and analyzing usage patterns; by using the app, you consent to the use of cookies as outlined in our Cookie Policy.")
        print()
    elif choice == 7:
        print("""
        Copyright (c) 2024 InCollege

        All rights reserved.

        This software, [App Name], is the property of InCollege. Any redistribution, modification, or reproduction is not permitted without the express consent of InCollege.
        """)
        print()

    elif choice == 8:
        print("InCollege app is committed to fostering inclusive education, providing a seamless and enriching experience for users of all abilities, promoting diversity, and ensuring a safe and supportive learning environment.")
        print()
    elif choice == 9:
        print("1. Language Preference")
        print("0. Exit")
        sub_choice = input("Enter your choice: ")
        if sub_choice == '1':
            if userData:
                handle_language_preference(userData, db)
                print()
            else:
                print("Log in to access Language Preference")
                print()
        elif sub_choice == '0':
            main_hub(userData, db)
        else:
            print("Invalid choice")
            print()

    else:
        print("Invalid choice")
        print()


def handle_language_preference(userData, db):
    print("Language Controls:")
    val = db.query(models.GuestControl).filter(
        models.GuestControl.user_id == userData.id).first()
    if val is None:
        # Create a new GuestControl record with default values
        val = models.GuestControl(user_id=userData.id, incollege_email_enabled=True,
                                  sms_enabled=True, targeted_advertising_enabled=True)
        db.add(val)
        db.commit()
    print("Select an option:")
    print("1. Language preference", val.language_preference)
    print("0. Exit")
    print()

    while True:
        print("Would you like to change your preference?")
        choice = input("Enter your choice: ")
        if choice.lower() == 'yes':
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
                print()
                explore_links(userData, db, "Important Links")
        elif choice.lower() == 'no':
            main_hub(userData, db)

        else:
            print("Invalid choice")
            handle_important_links_choice(userData, db, 9)


def handle_profile(userData, db):
    while True:
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == userData.id).first()

        if user_profile:
            print("\nProfile Menu:")
            print("1. View your profile")
            print("2. Edit your profile")
            print("3. View your friends' profiles")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                # Display the user's profile
                print(f"\n{userData.first_name} {userData.last_name}'s Profile:")
                print(f"Title: {user_profile.title}")
                print(f"Major: {user_profile.major}")
                print(f"University: {user_profile.university_name}")
                print(f"About: {user_profile.about_student}")

            elif choice == '2':
                # Edit the user's profile
                print("\nEnter new profile details (press enter to skip any field):")
                title = input("New title: ") or user_profile.title
                major = input("New major: ") or user_profile.major
                university = input(
                    "New university: ") or user_profile.university_name
                about = input("New about: ") or user_profile.about_student

                # Update the profile
                user_profile.title = title
                user_profile.major = major
                user_profile.university_name = university
                user_profile.about_student = about
                db.commit()
                print("Profile updated successfully.")

            elif choice == '3':
                # View friends' profiles
                friendships = db.query(models.Friendship).filter(or_(models.Friendship.user_id == userData.id,
                                                                 models.Friendship.friend_id == userData.id)).all()
                if friendships:
                    print("\nYour Friends:")
                    for friendship in friendships:
                        friend_id = friendship.friend_id if friendship.user_id == userData.id else friendship.user_id
                        friend = db.query(models.User).filter(
                            models.User.id == friend_id).first()
                        friend_profile = db.query(models.UserProfile).filter(
                            models.UserProfile.user_id == friend_id).first()

                        if friend_profile:
                            print(
                                f"\n{friend.first_name} {friend.last_name}'s Profile:")
                            print(f"Title: {friend_profile.title}")
                            print(f"Major: {friend_profile.major}")
                            print(
                                f"University: {friend_profile.university_name}")
                            print(f"About: {friend_profile.about_student}")
                        else:
                            print(
                                f"{friend.first_name} {friend.last_name} does not have a profile.")
                else:
                    print("You do not have any friends to view profiles.")

            elif choice == '0':
                print("Exiting profile menu.")
                break

            else:
                print("Invalid option. Please try again.")

        else:
            print("\nYou do not have a profile yet.")
            print("1. Create profile")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                # Create a new profile
                print("\nEnter your profile details:")
                title = input("Title: ")
                major = input("Major: ")
                university = input("University: ")
                about = input("About: ")

                new_profile = models.UserProfile(
                    user_id=userData.id,
                    title=title,
                    major=Profile.format_text(major),
                    university_name=Profile.format_text(university),
                    about_student=about
                )
                db.add(new_profile)
                db.commit()
                print("Profile created successfully.")

            elif choice == '0':
                print("Exiting profile menu.")
                break

            else:
                print("Invalid option. Please try again.")


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
            print("would you like to sign up now? (yes/no)")
            if input("Enter your choice: ").lower() != 'yes':
                main()
                print()
        else:
            print("Goodbye")
            main()
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
            else:
                signup(db)
                return "Username already in use"
        else:
            print("Not duplicate")  # I do not khow if it is needed
            print()
        premium = input("Would you like to purchase plus subscription for $10/mounth? With Plus Subscription, You have the ability to send messages to any user in the system, regardless of their friendship status,  communicate more freely and efficiently.  (yes/no): ")
        if premium.lower() == 'yes':
            premium = True
            one_month_from_now = datetime.now() + relativedelta(months=1)
            print("You have successfully upgraded to a premium user")

        else:
            premium = False
            one_month_from_now = None
            print("You have chosen not to upgrade to a premium user")
        print()
        hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()
        user_create = UserCreate(username=username, hashed_password=hashed_password,
                                 school=school, first_name=first_name, last_name=last_name, premium=premium, premium_until=one_month_from_now)
        new_user = models.User(**user_create.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = UserInfo(id=new_user.id, username=new_user.username, school=new_user.school,
                        first_name=new_user.first_name, last_name=new_user.last_name, premium=new_user.premium)
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

        existing_users = db.query(models.User).filter(
            models.User.id != new_user.id).all()

        for user in existing_users:
            notification = models.UserNotification(
                new_user_id=new_user.id, notified_user_id=user.id)
            db.add(notification)

        db.commit()

        skipVarforTest = main_hub(user, db)
        return "Test Completed"

    else:

        continue_signup = input(
            "Password is invalid. Do you want to continue signup? (yes/no): ")
        if continue_signup.lower() == 'yes':
            print()
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
            return "Not Successful Login"

    queryUser = db.query(models.User).filter(
        models.User.username == username).first()
    if queryUser is None:
        print("Sign Up first")
        print()
        main()
        return
    elif queryUser.hashed_password != password:
        print("Password is incorrect")
        print()
        main()
        return
    print("Login successfuly")
    user = UserInfo(id=queryUser.id, username=queryUser.username, school=queryUser.school,
                    first_name=queryUser.first_name, last_name=queryUser.last_name, premium=queryUser.premium)

    notifications = db.query(models.UserNotification).join(models.User, models.User.id == models.UserNotification.new_user_id).filter(
        models.UserNotification.notified_user_id == queryUser.id,
        models.UserNotification.delivered == False
    ).all()

    newMessages = db.query(models.Message).filter(models.Message.receiver_id ==
                                                  queryUser.id, models.Message.read == False).all()  # Messages notificaitons
    if not notifications and not newMessages:
        print("No new notifications.")

    elif notifications and not newMessages:
        for notification in notifications:
            new_user = db.query(models.User).filter_by(
                id=notification.new_user_id).first()
            print(f"{new_user.first_name} {new_user.last_name} has joined InCollege.")
            notification.delivered = True
    elif not notifications and newMessages:
        for message in newMessages:
            sender = db.query(models.User).filter(
                models.User.id == message.sender_id).first()
            print(
                f"You have a new message from {sender.first_name} {sender.last_name}.")
    elif notifications and newMessages:
        for notification in notifications:
            new_user = db.query(models.User).filter_by(
                id=notification.new_user_id).first()
            print(f"{new_user.first_name} {new_user.last_name} has joined InCollege.")
            notification.delivered = True
        print()
        for message in newMessages:
            sender = db.query(models.User).filter(
                models.User.id == message.sender_id).first()
            print(
                f"You have a new message from {sender.first_name} {sender.last_name}.")

    db.commit()
    print()
    main_hub(user, db)
    return "Successful Login"


def logout():
    print("Logout successful")
    main()
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
            print("6. Messages")
            print("7. Profile")
        print("5. Exit")
        initial_choice = input("Enter your choice: ").lower()

        if initial_choice == '5':
            print("Goodbye")
            print()
            main()
            break
        elif initial_choice == '1':
            print()
            explore_links(userData, db, "Useful Links")
        elif initial_choice == '2':
            print()
            explore_links(userData, db, "Important Links")
        elif initial_choice == '3':
            print()
            userData, db = user_actions(userData, db)
        elif initial_choice == '4':
            print()
            job_actions(userData, db)
        elif initial_choice == '6':
            print()
            message_handler(userData, db)
        elif initial_choice == '7':
            print()
            handle_profile(userData, db)
        else:
            print("Invalid choice")
            print()


def explore_links(userData, db, link_type):
    while True:
        if userData:
            print(f"Welcome, {userData.first_name}!")
            print()
        else:
            print("Welcome! (You are not logged in)")
            print()

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
            print()  # FIX SHOULD NOT WE GO TO MAIN HUB INSTEAD
            break
        elif link_type == "Useful Links" and choice in ('1', '2', '3', '4'):
            print()
            handle_useful_links_choice(userData, db, int(choice))
        elif link_type == "Important Links" and choice in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
            print()
            handle_important_links_choice(userData, db, int(choice))
        else:
            print("Invalid choice")
            print()


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
            print("8. Go to main hub")
            print("0. Exit")
            user_choice = input("Enter your choice: ").lower()

            if user_choice == '1':
                print()
                job_actions(userData, db)
                # pass I dunno why we had pass here
            elif user_choice == '2':
                print()
                find_new_friends_and_send_request(userData, db)
            elif user_choice == '3':
                print()
                learn_new_skills(userData, db)
            elif user_choice == '4':
                print()
                view_all_friends(userData, db)
                disconnect_choice = input(
                    "Do you want to disconnect from a friend? (yes/no): ")
                if disconnect_choice.lower() == 'yes':
                    friend_id_to_disconnect = int(
                        input("Enter the User ID of the friend you want to disconnect from: "))
                    disconnect_from_friend(
                        userData.id, friend_id_to_disconnect, db)
            elif user_choice == '5':
                print()
                handle_friend_requests(userData, db)
            elif user_choice == '6':
                logout()
            elif user_choice == '7':
                print()
                create_profile(userData, db)
            elif user_choice == '8':
                print()
                main_hub(userData, db)
            elif user_choice == '0':
                print("Goodbye")
                main()  # added
                print()
                break
            else:
                print("Invalid choice")
                print()
        else:
            print("You need to log in to perform user actions.")
            print()
            signup(db)

    return userData, db


# Fix it so it does not comeback to the main hub once user does not have friends
def view_all_friends(userData: UserInfo, db):

    friends = db.query(models.Friendship).filter(or_(models.Friendship.user_id == userData.id,
                                                     models.Friendship.friend_id == userData.id)).all()

    if not friends:
        print("You have no friends")
        print()
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
        print()
        main_hub(userData, db)
    else:
        print()
        user_actions(userData, db)
        return


def disconnect_from_friend(userData, friend_id: int, db: Session):
    friendship = db.query(models.Friendship).filter(
        ((models.Friendship.user_id == userData.id) & (models.Friendship.friend_id == friend_id)) |
        ((models.Friendship.user_id == friend_id) &
         (models.Friendship.friend_id == userData.id))
    ).first()

    if friendship:
        db.delete(friendship)
        db.commit()
        print("Successfully disconnected from the friend.")
        print()
    else:
        print("Friendship not found.")
        print()


def find_new_friends_and_send_request(userData: UserInfo, db):
    last_name_to_search = input("Enter the last name to search: ")
    matching_users = db.query(models.User).filter(
        models.User.last_name.like(f"%{last_name_to_search}%")).all()

    if not matching_users:
        print(f"No users found with the last name '{last_name_to_search}'.")
        print()
        main_hub(userData, db)
        return "No users found"

    print("Matching Users:")
    for user in matching_users:
        print(
            f"User ID: {user.id}, First Name: {user.first_name}, Last Name: {user.last_name}, School: {user.school}")

    user_id_to_add = input(
        "Enter the User ID you want to send a friend request to (or enter '0' to go back to the main hub): ")

    if user_id_to_add == '0':
        print()
        main_hub(userData, db)
        return "Return to Main Hub"

    try:
        user_id_to_add = int(user_id_to_add)
        if user_id_to_add == userData.id:
            print("You cannot send a friend request to yourself.")
            print()
            main_hub(userData, db)
            return "Cannot send friend request to self"
        # FIXED this function because Friendship.UserData_id is not a thing
        elif db.query(models.Friendship).filter(or_(
                and_(models.Friendship.user_id == userData.id,
                     models.Friendship.friend_id == user_id_to_add),
                and_(models.Friendship.user_id == user_id_to_add, models.Friendship.friend_id == userData.id))).first():
            print("Friendship already exists.")
            print()
        elif db.query(models.ProspectiveConnection).filter(
                models.ProspectiveConnection.caller_id == userData.id,
                models.ProspectiveConnection.receiver_id == user_id_to_add).first():
            print("Friend request already sent.")
            print()
            main_hub(userData, db)
            return "Friend request already sent"
        elif db.query(models.ProspectiveConnection).filter(
                models.ProspectiveConnection.receiver_id == userData.id,
                models.ProspectiveConnection.caller_id == user_id_to_add).first():
            print(
                "You have a pending friend request from this user. Please check your inbox.")
            print()
            main_hub(userData, db)
            return "Pending friend request exists"
        else:
            print()
            send_friend_request(userData.id, user_id_to_add, db)
            return "Successfully sent friend request."

    # Improved flow of the code because it will return in main after Invalid User ID
    except ValueError:
        print("Invalid User ID.")
        print("press 1 to try again")
        print("press anything else to go back to main hub")
        choice = input("Enter your choice: ")
        if choice == '1':
            find_new_friends_and_send_request(userData, db)
        else:
            main_hub(userData, db)
            return "Return to Main Hub 2"

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
            user_actions(userData, db)
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

            if choice == "1":
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


def create_profile(userData, db):
    # Check if the user already has a profile
    existing_profile = db.query(models.UserProfile).filter_by(
        models.UserProfile.user_id == userData.id).first()
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
        university_name=UserInfo.school,
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
        UserProfile.user_id == userData.id).first()
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
        userData.user_id == userData.id).first()
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
        print()
        main_hub(userData, db)
    else:
        print("Goodbye")
        print()
        main()
        return


def main():
    db = next(get_db())
    try:
        signup(db=db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
