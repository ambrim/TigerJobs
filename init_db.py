# File to reset database when needed
import sqlalchemy
import sqlalchemy.orm
import models
import os

db_url = os.getenv("DATABASE_URL")

# Add test internship
def add_test_internship(session):
    internship = models.Internships(
        netid = 'amkumar',
        title = 'Software Engineering Intern',
        location = 'Tampa, FL, USA',
        virtual = 'Hybrid',
        description = 'Worked for data science team',
        technologies = 'R, Google Colab, RedHat OpenShift',
        type = 'Internship: Industry - Public Sector',
        length = 10,
        company = 'MITRE',
        company_id = 1,
        company_type = 'STEM Research',
        salary = 25,
        supervisor = 1,
        pay = 2,
        balance = 3, 
        culture = 5,
        career_impact = 3,
        difficulty = 4,
        enjoyment = 3,
        upvotes = [],
        major = 'COS',
        certificates = 'SML, Finance',
        grade = 'so',
        date_created = '2023-01-10',
        reported = False
    )
    session.add(internship)

# Add test interview
def add_test_interview(session):
    interview = models.Interviews(
        netid = 'amkumar',
        round = 1,
        final_round = False,
        job_position = 'Software Development Engineer Intern',
        job_field = 'Software Engineering',
        type='Technical',
        location_type='Video',
        duration = '2 hours',
        company = 'Amazon',
        company_id = 2,
        num_interviewers= 1,
        question_description = 'Nothing',
        technologies = 'Coding language of your choice',
        how_interview = 'Application on website',
        tips = 'Leetcode',
        difficulty = 2,
        enjoyment = 4,
        advanced=True,
        upvotes = [],
        major = 'COS',
        certificates = 'Statistics and Machine Learning, Finance',
        grade = 'jr',
        date_created = '2023-01-10',
        reported = False
    )
    session.add(interview)

# Add test companies
def add_test_companies(session):
    company = models.Companies(
        name = 'MITRE',
        num_interviews = 0,
        num_internships = 1,
        interview_difficulty = 0,
        interview_enjoyment = 0,
        internship_supervisor = 1,
        internship_pay = 2,
        internship_balance = 3,
        internship_culture = 5,
        internship_career = 3,
        internship_difficulty = 4,
        internship_enjoyment = 3,
        locations=['Tampa, FL, USA'],
        location_count=[1],
        fields=['STEM Research'],
        field_count=[1],
        majors=['COS'],
        major_count=[1],
        interview_grades=[0, 0, 0, 0, 0],
        internship_grades=[0, 1, 0, 0, 0],
        advanced = 0,
        enjoyed_interview = 0,
        enjoyed_internship = 1,
        difficult_interview = 0,
        difficult_internship = 1,
        reported = False
    )
    session.add(company)
    company = models.Companies(
        name = 'Amazon',
        num_interviews = 1,
        num_internships = 0,
        interview_difficulty = 2,
        interview_enjoyment = 4,
        internship_supervisor = 0,
        internship_pay = 0,
        internship_balance = 0,
        internship_culture = 0,
        internship_career = 0,
        internship_difficulty = 0,
        internship_enjoyment = 0,
        locations=[],
        location_count=[],
        fields=['Software Engineering'],
        field_count=[1],
        majors=['COS'],
        major_count=[1],
        interview_grades=[0, 0, 1, 0, 0],
        internship_grades=[0, 0, 0, 0, 0],
        advanced = 1,
        enjoyed_interview = 1,
        enjoyed_internship = 0,
        difficult_interview = 0,
        difficult_internship = 0,
        reported = False
    )
    session.add(company)

# Add test users
def add_test_users(session):
    user = models.Users(
        netid = "amkumar",
        major = '',
        certificates = '',
        grade = '',
        admin = False
    )
    session.add(user)

def main():
    # Create engine and drop and recreate all tables
    engine = sqlalchemy.create_engine(db_url)
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

    with sqlalchemy.orm.Session(engine) as session:
        # Add fake test data if needed
        add_test_internship(session)
        add_test_interview(session)
        add_test_companies(session)
        add_test_users(session)
        session.commit()
        
    engine.dispose()

if __name__ == '__main__':
    main()


