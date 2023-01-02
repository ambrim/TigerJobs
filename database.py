from typing import List
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError
import models
import os

# Database URL
db_url = os.getenv("DATABASE_URL")
# Global engine to use
engine =  sqlalchemy.create_engine(db_url, pool_pre_ping=True)
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
            models.Internships.id == id).first()
    return company
# Delete a company
def delete_company(id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Companies).filter(
            models.Companies.id == id).delete()
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
# Delete a user
def delete_user(netid):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Users).filter(
            models.Users.netid == netid).delete()
        session.commit()