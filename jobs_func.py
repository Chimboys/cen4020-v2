from user import UserInfo
import models
from sqlalchemy.exc import SQLAlchemyError


def job_actions(userData, db):
    while True:
        print("1. Show jobs")
        print("2. Post a job")
        print("3. Apply to a job")
        print("4. Delete posted job")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_all_jobs(userData, db)
        elif choice == "2":
            post_a_job(userData, db)
        elif choice == "3":
            apply_for_job(userData, db)
        elif choice == "4":
            delete_posted_job(userData, db)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def show_all_jobs(userData, db):
    print("Would you like to see:")
    print("1. Jobs you've applied for")
    print("2. Jobs you haven't applied for")
    print("3. All jobs")
    user_choice = input("Enter your choice (1/2/3): ")

    applied_jobs_ids = db.query(models.JobApplication.job_post_id).filter_by(
        user_id=userData.id).all()
    applied_jobs_ids = [id[0]
                        for id in applied_jobs_ids]  # Flatten the list of tuples

    if user_choice == '1':
        # Fetch only the jobs the user has applied for
        jobs_to_display = db.query(models.JobPost).filter(
            models.JobPost.id.in_(applied_jobs_ids)).all()
    elif user_choice == '2':
        # Fetch jobs the user hasn't applied for
        jobs_to_display = db.query(models.JobPost).filter(
            ~models.JobPost.id.in_(applied_jobs_ids)).all()
    elif user_choice == '3':
        # Display all jobs
        jobs_to_display = db.query(models.JobPost).all()
    else:
        print("Invalid choice. Showing all jobs by default.")
        jobs_to_display = db.query(models.JobPost).all()

    # Display the filtered list of jobs
    if not jobs_to_display:
        print("No jobs to display based on your selection.")
        return

    for count, job in enumerate(jobs_to_display, start=1):
        print(f"{count}. Title: {job.title}")
        # Optionally, indicate if the user has applied for each job
        if job.id in applied_jobs_ids:
            print("You have applied for this job")
        print()  # Blank line for readability

    print("End of job list\n")
    print("Which job would you like more information on? (Enter the job number or type 'exit' to return to the Job actions.)")

    while True:
        choice = input("Enter your choice: ")
        if choice.lower() == 'exit':
            break
        try:
            job_number = int(choice)
            if job_number < 1 or job_number > len(jobs_to_display):
                print("Invalid job number. Please try again.")
                continue
            selected_job = jobs_to_display[job_number - 1]
            print(f"Title: {selected_job.title}")
            print(f"Description: {selected_job.description}")
            print(f"Employer: {selected_job.employer}")
            print(f"Location: {selected_job.location}")
            if selected_job.salary:
                print(f"Salary: {selected_job.salary}")
            else:
                print("Salary: Not specified")
            print()
            break
        except ValueError:
            print(
                "Invalid input. Please enter a number or 'exit' to return to the Job actions.")


def apply_for_job(userData, db):
    jobs = db.query(models.JobPost).all()
    for job in jobs:
        print(f"Job ID: {job.id}, Title: {job.title}")
    job_id = input("Enter the job ID you want to apply for: ")
    job = db.query(models.JobPost).filter_by(id=job_id).first()

    if not job:
        print("Invalid job ID. Please try again.")
        return

    application = models.JobApplication(
        user_id=userData.id, job_post_id=job_id)
    db.add(application)
    db.commit()

    print("Application submitted successfully.")


def post_a_job(userData: UserInfo, db):
    # Check the current number of job postings
    job_count = db.query(models.JobPost).count()
    if job_count >= 10:
        print("The system can only support 10 job postings. Please try again later.")

    else:
        while True:
            try:
                title = input("Enter the title of the job: ")
                description = input("Enter the description of the job: ")
                employer = input("Enter the employer name: ")
                location = input("Enter the location of the job: ")
                salary_input = input(
                    "Enter the salary for the job (or leave blank if not applicable): ")
                salary = None if salary_input.strip() == "" else int(salary_input)

                # Create a new job post
                post = models.JobPost(
                    title=title,
                    description=description,
                    employer=employer,
                    location=location,
                    salary=salary,
                    user_id=userData.id
                )
                db.add(post)
                db.commit()
                print("Job posted\n")

                # Re-check the job count after posting
                job_count = db.query(models.JobPost).count()
                if job_count >= 10:
                    print(
                        "Job posting limit reached. No more jobs can be posted at this time.")
                    break

                # Ask the user if they want to post another job
                choice = input("Do you want to post another job? (yes/no): ")
                if choice.lower() == 'no':
                    break
            except SQLAlchemyError as e:
                print(f"Error posting job: {e}")
                choice = input(
                    "Would you like to go back to the main hub? (yes/no): ")
                if choice.lower() == 'yes':
                    break
                else:
                    print("Re-enter details\n")


def delete_posted_job(userData, db):
    # Fetch jobs posted by the user
    posted_jobs = db.query(models.JobPost).filter_by(user_id=userData.id).all()

    if not posted_jobs:
        print("You haven't posted any jobs.")
        return

    while True:
        posted_jobs = db.query(models.JobPost).filter_by(
            user_id=userData.id).all()
        print("Jobs posted by you:")
        for job in posted_jobs:
            print(f"ID: {job.id}, Title: {job.title}")

        job_id = input(
            "Enter the ID of the job you want to delete (or 'exit' to return to the Job actions): ")

        if job_id.lower() == 'exit':
            break

        job = db.query(models.JobPost).filter_by(
            id=job_id, user_id=userData.id).first()

        if not job:
            print("Invalid job ID. Please try again.")
            continue

        db.delete(job)
        db.commit()

        print("Job deleted successfully.")
