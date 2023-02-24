import sqlalchemy.ext.declarative
import sqlalchemy
from sqlalchemy.dialects.postgresql import ARRAY

Base = sqlalchemy.ext.declarative.declarative_base()
# MIGHT WANT TO MOVE UPVOTING INTO REVIEWS THEMSELVES NOT IN USER
# Interviews Review Table
class Interviews (Base):
    __tablename__ = 'interviews'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # User posting review
    netid = sqlalchemy.Column(sqlalchemy.String)
    # 1, 2, 3, or 4 (4 is 4th or later)
    round = sqlalchemy.Column(sqlalchemy.Integer)
    # True if final round
    final_round = sqlalchemy.Column(sqlalchemy.Boolean)
    # Job Position
    job_position = sqlalchemy.Column(sqlalchemy.String)
    # Job Field
    job_field = sqlalchemy.Column(sqlalchemy.String)
    # Type of interview (OA, Screening, Behavioral, Technical, other)
    type = sqlalchemy.Column(sqlalchemy.String)
    # Location type (in-person, video, phone, or unsupervised)
    location_type = sqlalchemy.Column(sqlalchemy.String)
    # Duration of interview
    duration = sqlalchemy.Column(sqlalchemy.String)
    # Company Name
    company = sqlalchemy.Column(sqlalchemy.String)
    # Company ID
    company_id = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of interviewers
    num_interviewers = sqlalchemy.Column(sqlalchemy.Integer)
    # Questions asked
    question_description = sqlalchemy.Column(sqlalchemy.String)
    # Technologies required for interview
    technologies = sqlalchemy.Column(sqlalchemy.String)
    # How user got interview
    how_interview = sqlalchemy.Column(sqlalchemy.String)
    # Tips for preparation
    tips = sqlalchemy.Column(sqlalchemy.String)
    # Difficulty from 1 to 5
    difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Enjoyment of interview process from 1 to 5
    enjoyment = sqlalchemy.Column(sqlalchemy.Integer)
    # Advanced/got offer
    advanced = sqlalchemy.Column(sqlalchemy.Boolean)
    # Upvoting users
    upvotes = sqlalchemy.Column(ARRAY(sqlalchemy.String))
    # User's major
    major = sqlalchemy.Column(sqlalchemy.String)
    # User's certificates
    certificates = sqlalchemy.Column(sqlalchemy.String)
    # User's class (fr, so, jr, sr, grad, other)
    grade = sqlalchemy.Column(sqlalchemy.String)
    # Date created (yyyy-mm-dd)
    date_created = sqlalchemy.Column(sqlalchemy.String)
    # True if this interview was reported for offensive content
    reported = sqlalchemy.Column(sqlalchemy.Boolean)

# Interships Review Table
class Internships (Base):
    __tablename__ = 'internships'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # User posting review
    netid = sqlalchemy.Column(sqlalchemy.String)
    # Internship title
    title = sqlalchemy.Column(sqlalchemy.String)
    # Location of internship
    location = sqlalchemy.Column(sqlalchemy.String)
    # Virtual, hybrid, or in-person
    virtual = sqlalchemy.Column(sqlalchemy.String)
    # Internship description
    description = sqlalchemy.Column(sqlalchemy.String)
    # Technologies used description
    technologies = sqlalchemy.Column(sqlalchemy.String)
    # Internship type
    type = sqlalchemy.Column(sqlalchemy.String)
    # Length of internship in months
    length = sqlalchemy.Column(sqlalchemy.Integer)
    # Company Name
    company = sqlalchemy.Column(sqlalchemy.String)
    # Company ID
    company_id = sqlalchemy.Column(sqlalchemy.Integer)
    # Type of company
    company_type = sqlalchemy.Column(sqlalchemy.String)
    # Internship salary per hour
    salary = sqlalchemy.Column(sqlalchemy.Integer)
    # Supervisor Rating (1 to 5)
    supervisor = sqlalchemy.Column(sqlalchemy.Integer)
    # Pay Rating (1 to 5)
    pay = sqlalchemy.Column(sqlalchemy.Integer)
    # Work/Life Balance Rating (1 to 5)
    balance = sqlalchemy.Column(sqlalchemy.Integer)
    # Culture Rating (1 to 5)
    culture = sqlalchemy.Column(sqlalchemy.Integer)
    # Career Impact Rating (1 to 5)
    career_impact = sqlalchemy.Column(sqlalchemy.Integer)
    # Difficulty of internship (1 to 5)
    difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Enjoyment of internship (1 to 5)
    enjoyment = sqlalchemy.Column(sqlalchemy.Integer)
    # Upvoting users
    upvotes = sqlalchemy.Column(ARRAY(sqlalchemy.String))
    # User's major
    major = sqlalchemy.Column(sqlalchemy.String)
    # User's certificates
    certificates = sqlalchemy.Column(sqlalchemy.String)
    # User's class (fr, so, jr, or sr)
    grade = sqlalchemy.Column(sqlalchemy.String)
    # Date created (yyyy-mm-dd)
    date_created = sqlalchemy.Column(sqlalchemy.String)
    # True if this interview was reported for offensive content
    reported = sqlalchemy.Column(sqlalchemy.Boolean)

# Companies Table
class Companies (Base):
    __tablename__ = 'companies'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # Name of company 
    name = sqlalchemy.Column(sqlalchemy.String)
    # Number of interview reviews
    num_interviews = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of internship reviews
    num_internships = sqlalchemy.Column(sqlalchemy.Integer)
    # Interview difficulty rating
    interview_difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Interview enjoyment rating
    interview_enjoyment = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship Supervisor Rating (1 to 5)
    internship_supervisor = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship Pay Rating (1 to 5)
    internship_pay = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship Work/Life Balance Rating (1 to 5)
    internship_balance = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship Culture Rating (1 to 5)
    internship_culture = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship Career Impact Rating (1 to 5)
    internship_career = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship difficulty rating
    internship_difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship enjoyment rating
    internship_enjoyment = sqlalchemy.Column(sqlalchemy.Integer)
    # Set of locations added
    locations = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
    # Review count by location
    location_count = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
    # Set of fields added to company
    fields = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
    # Review count by field
    field_count = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
    # Set of majors
    majors = sqlalchemy.Column(ARRAY(sqlalchemy.String))
    # Review count by major
    major_count = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
    # Grade distribution for interviews
    interview_grades = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
    # Grade distribution for internships
    internship_grades = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
    # Number of interview people that advanced
    advanced = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of people that enjoyed interview
    enjoyed_interview = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of people that enjoyed job
    enjoyed_internship = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of people that found interview difficult
    difficult_interview = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of people that found job difficult
    difficult_internship = sqlalchemy.Column(sqlalchemy.Integer)
    # True if this interview was reported for offensive content
    reported = sqlalchemy.Column(sqlalchemy.Boolean)

# Users Table
class Users (Base):
    __tablename__ = 'users'
    # NetID of user
    netid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    # User's major
    major = sqlalchemy.Column(sqlalchemy.String)
    # User's certificates
    certificates = sqlalchemy.Column(sqlalchemy.String)
    # User's class (fr, so, jr, or sr)
    grade = sqlalchemy.Column(sqlalchemy.String)
    # True if user is admin
    admin = sqlalchemy.Column(sqlalchemy.Boolean)