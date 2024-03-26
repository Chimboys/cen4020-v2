from user import UserInfo


def job_actions(userData, db):
    while True:
        print("1. Show all jobs")
        print("2. Post a job")
        print("3. Create a job")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_all_jobs()
        elif choice == "2":
            post_job()
        elif choice == "3":
            create_job()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def show_all_jobs():
    # Code to retrieve and display all jobs from the database
    pass


def apply_for_job(userData, db):
    # Code to apply for a job
    pass


def post_a_job(userData: UserInfo, db):
    # Check the current number of job postings
    job_count = db.query(models.Post).count()
    if job_count >= 10:
        print("The system can only support 10 job postings. Please try again later.")
        # Assuming you want to return to the main hub
        return main_hub(userData, db)

    while True:
        try:
            title = input("Enter the title of the job: ")
            content = input("Enter the content of the job: ")
            # Create a new job post
            post = models.Post(title=title, content=content,
                               user_id=userData.id)
            db.add(post)
            db.commit()
            print("Job posted\n")

            # Re-check the job count after posting
            job_count = db.query(models.Post).count()
            if job_count >= 10:
                print(
                    "Job posting limit reached. No more jobs can be posted at this time.")
                return main_hub(userData, db)

            # Ask the user if they want to post another job
            choice = input("Do you want to post another job? (yes/no): ")
            if choice.lower() == 'no':
                return main_hub(userData, db)

        except SQLAlchemyError as e:
            print(f"Error posting job: {e}")
            choice = input(
                "Would you like to go back to the main hub? (yes/no): ")
            if choice.lower() == 'yes':
                return main_hub(userData, db)
            else:
                print("Re-enter details\n")
