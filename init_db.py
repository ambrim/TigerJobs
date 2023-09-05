# File to reset database when needed
import sqlalchemy
import sqlalchemy.orm
import models
import os

db_url = os.getenv("DATABASE_URL")

# If you need to manually add something, update the fields below according
# to the Instructions for Updating TigerJobs document
# For info on the fields, look at the TigerJobs Programmer's Guide

# def add_test_user(session):
#     user = models.Users(
#         netid = ,
#         major = ,
#         certificates = ,
#         grade = ,
#         admin = ,
#     )
#     session.add(user)

# def add_test_company(session):
#     company = models.Companies(
#         name = ,
#         num_interviews = ,
#         num_internships = ,
#         interview_difficulty = ,
#         interview_enjoyment = ,
#         internship_supervisor = ,
#         internship_pay = ,
#         internship_balance = ,
#         internship_culture = ,
#         internship_career = ,
#         internship_difficulty = ,
#         internship_enjoyment = ,
#         locations= [],
#         location_count= [],
#         fields= [],
#         field_count=[],
#         majors= [],
#         major_count=[],
#         interview_grades = [0, 0, 0, 0, 0],
#         internship_grades = [0, 0, 0, 0, 0],
#         advanced = ,
#         enjoyed_interview = ,
#         enjoyed_internship = ,
#         difficult_interview = ,
#         difficult_internship = ,
#         reported = 
#     )
#     session.add(company)

# def add_test_job(session):
#     internship = models.Internships(
#         netid = ,
#         title = ,
#         location = ,
#         virtual = ,
#         description = ,
#         technologies = ,
#         type = ,
#         length = ,
#         company = ,
#         company_id = ,
#         company_type = ,
#         salary = ,
#         supervisor = ,
#         pay = ,
#         balance = ,
#         culture = ,
#         career_impact = ,
#         difficulty = ,
#         enjoyment = ,
#         upvotes = [],
#         major = ,
#         certificates = ,
#         grade = ,
#         date_created = ,
#         reported = 
#     )
#     session.add(internship)

# def add_test_interview(session):
#     interview = models.Interviews(
#         # Update interview info here
#         netid = ,
#         round = ,
#         final_round = ,
#         job_position = ,
#         job_field = ,
#         type= ,
#         location_type= ,
#         duration = ,
#         company = ,
#         company_id = ,
#         num_interviewers = ,
#         question_description = ,
#         technologies = ,
#         how_interview = ,
#         tips = ,
#         difficulty = ,
#         enjoyment = ,
#         advanced = ,
#         upvotes = [],
#         major = ,
#         certificates = ,
#         grade = ,
#         date_created = ,
#         reported = 
#     )
#     session.add(interview)

def main():
    # Create engine and drop and recreate all tables
    engine = sqlalchemy.create_engine(db_url)
    models.Base.metadata.create_all(engine)

    with sqlalchemy.orm.Session(engine) as session:
        # Add whatever you need here and uncomment corresponding functions above
        # add_test_user(session)
        # add_test_company(session)
        # add_test_job(session)
        # add_test_interview(session)
        session.commit()

    engine.dispose()

if __name__ == '__main__':
    main()