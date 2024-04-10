from models import UserProfile, Experience, Education
class Profile:
    def __init__(self, db_profile=None):
        if db_profile:
            # Initialize from an existing database profile
            self.user_id = db_profile.user_id
            self.title = db_profile.title
            self.major = db_profile.major
            self.university = db_profile.university_name
            self.about = db_profile.about_student
        else:
            # Initialize an empty profile
            self.user_id = None
            self.title = None
            self.major = None
            self.university = None
            self.about = None
        self.experiences = []  # To be filled with experience objects or data
        self.educations = []  # To be filled with education objects or data

    @staticmethod
    def format_text(text):
        """Format text to have each word start with an uppercase letter."""
        return ' '.join(word.capitalize() for word in text.split()) if text else None

    def display_profile(self):
        """Print out the profile details."""
        print(f"Title: {self.title}")
        print(f"Major: {self.major}")
        print(f"University: {self.university}")
        print(f"About: {self.about}")
        # Additional logic to display experiences and educations can be added here

    def update_or_create_profile(self, session, user_id, title, major, university, about):
        """Update an existing profile or create a new one."""
        self.user_id = user_id
        self.title = title
        self.major = self.format_text(major)
        self.university = self.format_text(university)
        self.about = about

        existing_profile = session.query(UserProfile).filter_by(user_id=self.user_id).first()
        if existing_profile:
            # Update existing profile
            existing_profile.title = self.title
            existing_profile.major = self.major
            existing_profile.university_name = self.university
            existing_profile.about_student = self.about
        else:
            # Create a new profile
            new_profile = UserProfile(
                user_id=self.user_id,
                title=self.title,
                major=self.major,
                university_name=self.university,
                about_student=self.about
            )
            session.add(new_profile)
        session.commit()

    def add_experience(self, title, employer, start_date, end_date, location, description, session):
        """Add an experience to the profile and save it to the database."""
        new_experience = Experience(
            title=title,
            employer=employer,
            date_started=start_date,
            date_ended=end_date,
            location=location,
            description=description,
            user_profile_id=self.user_id
        )
        session.add(new_experience)
        session.commit()

    def add_education(self, school_name, degree, years_attended, session):
        """Add an education detail to the profile and save it to the database."""
        new_education = Education(
            school_name=school_name,
            degree=degree,
            years_attended=years_attended,
            user_profile_id=self.user_id
        )
        session.add(new_education)
        session.commit()