import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

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
    # Duration of interview
    duration = sqlalchemy.Column(sqlalchemy.String)
    # Company Name
    company = sqlalchemy.Column(sqlalchemy.String)
    # Questions asked
    question_description = sqlalchemy.Column(sqlalchemy.String)
    # How user got interview
    how_interview = sqlalchemy.Column(sqlalchemy.String)
    # Tips for preparation
    tips = sqlalchemy.Column(sqlalchemy.String)
    # Difficulty from 1 to 5
    difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Enjoyment of interview process from 1 to 5
    enjoyment = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of upvotes
    upvotes = sqlalchemy.Column(sqlalchemy.Integer)
    # User's major
    major = sqlalchemy.Column(sqlalchemy.String)
    # User's certificates
    certificates = sqlalchemy.Column(sqlalchemy.String)
    # User's class (fr, so, jr, sr, grad, other)
    grade = sqlalchemy.Column(sqlalchemy.String)

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
    # Internship description
    description = sqlalchemy.Column(sqlalchemy.String)
    # Internship type
    type = sqlalchemy.Column(sqlalchemy.String)
    # Length of internship in months
    length = sqlalchemy.Column(sqlalchemy.Integer)
    # Company Name
    company = sqlalchemy.Column(sqlalchemy.String)
    # Type of company
    company_type = sqlalchemy.Column(sqlalchemy.String)
    # Internship salary per hour
    salary = sqlalchemy.Column(sqlalchemy.Integer)
    # Difficulty of internship (1 to 5)
    difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Enjoyment of internship (1 to 5)
    enjoyment = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of upvotes
    upvotes = sqlalchemy.Column(sqlalchemy.Integer)
    # User's major
    major = sqlalchemy.Column(sqlalchemy.String)
    # User's certificates
    certificates = sqlalchemy.Column(sqlalchemy.String)
    # User's class (fr, so, jr, or sr)
    grade = sqlalchemy.Column(sqlalchemy.String)


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
    # Internship difficulty rating
    internship_difficulty = sqlalchemy.Column(sqlalchemy.Integer)
    # Internship enjoyment rating
    internship_enjoyment = sqlalchemy.Column(sqlalchemy.Integer)

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
    # Upvoted interview reviews
    interview_upvotes = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
    # Favorited internship reviews
    internship_upvotes = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Integer))
