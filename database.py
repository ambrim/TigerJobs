from typing import List, Tuple
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import models
import os

# Database URL
db_url = os.getenv("DATABASE_URL")
# Global engine to use
engine =  sqlalchemy.create_engine(db_url, pool_pre_ping=True)
#----------------------------------------------------------------------
# Global Variables
#----------------------------------------------------------------------
majors = {
   'AAS': 'African American Studies (AAS)', 'ANT': 'Anthropology (ANT)',
   'ARC': 'Architecture (ARC)', 'ART': 'Art and Archaeology (ART)', 
   'AST': 'Astrophysical Sciences (AST)', 'CBE': 'Chemical and Biological Engineering (CBE)',
   'CHM': 'Chemistry (CHM)', 'CEE': 'Civil and Environmental Engineering (CEE)',
   'CLA': 'Classics (CLA)', 'COM': 'Comparative Literature (COM)', 
   'COS': 'Computer Science (COS)', 'EAS': 'East Asian Studies (EAS)',
   'EEB': 'Ecology and Evolutionary Biology (EEB)', 'ECO': 'Economics (ECO)',
   'ECE': 'Electrical and Computer Engineering (ECE)', 'ENG': 'English (ENG)',
   'FRE': 'French (FRE)', 'GEO': 'Geosciences (GEO)', 'GER': 'German (GER)',
   'HIS': 'History (HIS)', 'ITA': 'Italian (ITA)', 'MAT': 'Mathematics (MAT)',
   'MAE': 'Mechanical and Aerospace Engineering (MAE)', 'MOL': 'Molecular Biology (MOL)',
   'MUS': 'Music (MUS)', 'NES': 'Near Eastern Studies (NES)', 'NEU': 'Neuroscience (NEU)',
   'ORF': 'Operations Research and Financial Engineering (ORF)', 'PHI': 'Philosophy (PHI)',
   'PHY': 'Physics (PHY)', 'POL': 'Politics (POL)', 'POR': 'Portuguese (POR)', 
   'PSY': 'Psychology (PSY)', 'SPI': 'Public Policy/School of Public and International Affairs (SPI)',
   'REL': 'Religion (REL)', 'SLA': 'Slavic Languages and Literatures (SLA)',
   'SOC': 'Sociology (SOC)', 'SPA': 'Spanish (SPA)'
}
certificates = [
    'African American Studies', 'African Studies', 'American Studies',
    'Applications of Computing', 'Applied and Computational Mathematics',
    'Archaeology', 'Architecture and Engineering', 'Asian American Studies',
    'Biophysics', 'Cognitive Science', 'Contemporary European Politics and Society',
    'Creative Writing', 'Dance', 'East Asian Studies', 'Engineering Biology',
    'Engineering Physics', 'Entrepreneurship', 'Environmental Studies', 
    'European Cultural Studies', 'Finance', 'Gender and Sexuality Studies', 
    'Geological Engineering', 'Global Health and Health Policy', 'Hellenic Studies',
    'History and the Practice of Diplomacy', 'Humanistic Studies', 'Jazz Studies',
    'Journalism', 'Judaic Studies', 'Language and Culture', 'Latin American Studies',
    'Latino Studies', 'Linguistics', 'Materials Science and Engineering', 
    'Medieval Studies', 'Music Performance', 'Music Theater', 'Near Eastern Studies',
    'Neuroscience', 'Optimization and Quantitative Decision Science', 
    'Planets and Life', 'Quantitative and Computational Biology', 
    'Robotics and Intelligent Systems', 'Russian, East European and Eurasian Studies',
    'South Asian Studies', 'Statistics and Machine Learning', 'Sustainable Energy',
    'Teacher Preparation', 'Technology and Society', 'Theater',
    'Translation and Intercultural Communication', 'Urban Studies',
    'Values and Public Life', 'Visual Arts'
]
#----------------------------------------------------------------------
# Interview Review Queries
#----------------------------------------------------------------------
# Get all interview reviews
def get_all_interviews() -> List[models.Interviews]:
    interviews = []
    with sqlalchemy.orm.Session(engine) as session:
        interviews = session.query(models.Interviews).all()
    return interviews

##### HAVE TO ADD FILTER QUERIES TOO #####

# Add interview review to database
def add_interview(interview:models.Interviews):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(interview)
        session.commit()
# Get interview review from id
def get_interview(id) -> models.Interviews:
    # Make sure to only get one
    interview = None
    with sqlalchemy.orm.Session(engine) as session:
        interview = session.query(models.Interviews).filter(
            models.Interviews.id == id).first()
    return interview
# Delete an interview review
def delete_interview(id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Interviews).filter(
            models.Interviews.id == id).delete()
        session.commit()
#----------------------------------------------------------------------
# Internship Review Queries
#----------------------------------------------------------------------
# Get all internship reviews
def get_all_internships() -> List[models.Internships]:
    internships = []
    with sqlalchemy.orm.Session(engine) as session:
        internships = session.query(models.Internships).all()
    return internships

##### HAVE TO ADD FILTER QUERIES TOO #####

# Search for internship (Using get_all currently)
MAX_QUERY_LENGTH = 200 # not used currently
def search_for_internship(query):
    if query is None or not isinstance(query, str):
        return None, ""
    res = []
    with sqlalchemy.orm.Session(engine) as session:
        res = session.query(models.Internships).all()
    return res

# Add internship review to database
def add_internship(internship:models.Internships):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(internship)
        session.commit()
# Get internship review from id
def get_internship(id) -> models.Internships:
    # Make sure to only get one
    internship = None
    with sqlalchemy.orm.Session(engine) as session:
        internship = session.query(models.Internships).filter(
            models.Internships.id == id).first()
    return internship
# Delete an internship review
def delete_internship(id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Internships).filter(
            models.Internships.id == id).delete()
        session.commit()
#----------------------------------------------------------------------
# Company Queries
#----------------------------------------------------------------------
# Get all companies
def get_all_companies() -> List[models.Companies]:
    companies = []
    with sqlalchemy.orm.Session(engine) as session:
        companies = session.query(models.Companies).all()
    return companies

# Get all companies names
def get_all_company_names():
    companies = []
    company_names = []
    with sqlalchemy.orm.Session(engine) as session:
        companies = session.query(models.Companies).all()
    for company in companies:
        company_names.append(company.name)
    return company_names

##### HAVE TO ADD FILTER QUERIES TOO #####

# Add company to database
def add_company(company:models.Companies):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(company)
        session.commit()
# Get company from id
def get_company(id) -> models.Companies:
    # Make sure to only get one company
    company = None
    with sqlalchemy.orm.Session(engine) as session:
        company = session.query(models.Companies).filter(
            models.Companies.id == id).first()
    return company
# Get company from name
def get_company_by_name(name) -> models.Companies:
    # Make sure to only get one company
    company = None
    with sqlalchemy.orm.Session(engine) as session:
        company = session.query(models.Companies).filter(
            models.Companies.name.ilike(name)).first()
    return company
# Delete a company
def delete_company(id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Companies).filter(
            models.Companies.id == id).delete()
        session.commit()
# Update company
def update_company(company:models.Companies):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Companies).filter(
            models.Companies.id == company.id).update(
                {
                    'name': company.name,
                    'num_interviews': company.num_interviews,
                    'num_internships': company.num_internships,
                    'interview_difficulty': company.interview_difficulty,
                    'interview_enjoyment': company.interview_enjoyment,
                    'internship_supervisor': company.internship_supervisor,
                    'internship_pay': company.internship_pay,
                    'internship_balance': company.internship_balance,
                    'internship_culture': company.internship_culture,
                    'internship_career': company.internship_career,
                    'internship_difficulty': company.internship_difficulty,
                    'internship_enjoyment': company.internship_enjoyment
                }
            )
        session.commit()
#----------------------------------------------------------------------
# User Queries
#----------------------------------------------------------------------
# Add user to database
def add_user(user:models.Users):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(user)
        session.commit()
# Get user from netid
def get_user(netid) -> models.Users:
    # Make sure to only get one user
    user = None
    with sqlalchemy.orm.Session(engine) as session:
        company = session.query(models.Users).filter(
            models.Users.netid == netid).first()
    return company
# Update user
def update_user(user:models.Users):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Users).filter(
            models.Users.netid == user.netid).update(
                {
                    'netid': user.netid,
                    'major': user.major,
                    'certificates': user.certificates,
                    'grade': user.grade
                }
            )
        session.commit()
# Delete a user
def delete_user(netid):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Users).filter(
            models.Users.netid == netid).delete()
        session.commit()
# Get all reviews by user
def get_reviews_by_user(netid):
    interviews = []
    with sqlalchemy.orm.Session(engine) as session:
        interviews = session.query(models.Interviews).filter(
            models.Interviews.netid == netid
        ).all()
    internships = []
    with sqlalchemy.orm.Session(engine) as session:
        internships = session.query(models.Internships).filter(
            models.Internships.netid == netid
        ).all()
    return (interviews, internships)
    