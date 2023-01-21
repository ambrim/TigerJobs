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
        interviews = session.query(models.Interviews).order_by(
            models.Interviews.date_created.desc(),
            sqlalchemy.func.cardinality(models.Interviews.upvotes).desc(),
            models.Interviews.difficulty.desc(),
            models.Interviews.enjoyment.desc()
        ).all()
    return interviews

# Get interviews by filter
'''
    Filters list is as follows:
    [
        Query, Difficulty List, Enjoyment List, Class Year,
        Location Types, Interview Type, Interview Outcomes,
        Interview Final, Interview Durations, How Interviews,
        Majors, Certificates, Job Fields, Sort By Type, Sort By Direction
    ]
'''
def get_filtered_interviews(filters) -> List[models.Interviews]:
    interviews = []
    clauses = [models.Interviews.certificates.contains(elem) for elem in filters[11]]
    # Create sort by clauses
    sort_by_clauses = []
    if filters[13] == "recency" and filters[14]:
        sort_by_clauses.append(models.Interviews.date_created.desc())
    elif filters[13] == "recency" and not filters[14]:
        sort_by_clauses.append(models.Interviews.date_created)
    if filters[13] == "upvotes" and filters[14]:
        sort_by_clauses.append(sqlalchemy.func.cardinality(models.Interviews.upvotes).desc())
    elif filters[13] == "upvotes" and not filters[14]:
        sort_by_clauses.append(sqlalchemy.func.cardinality(models.Interviews.upvotes))
    if filters[13] == "difficulty" and filters[14]:
        sort_by_clauses.append(models.Interviews.difficulty.desc())
    elif filters[13] == "difficulty" and not filters[14]:
        sort_by_clauses.append(models.Interviews.difficulty)
    if filters[13] == "enjoyment" and filters[14]:
        sort_by_clauses.append(models.Interviews.enjoyment.desc())
    elif filters[13] == "enjoyment" and not filters[14]:
        sort_by_clauses.append(models.Interviews.enjoyment)
    with sqlalchemy.orm.Session(engine) as session:
        interviews = session.query(models.Interviews).filter(
            # Filter by query in title, description, technology, or company
            sqlalchemy.or_(
                models.Interviews.job_position.ilike('%{}%'.format(filters[0])),
                models.Interviews.company.ilike('%{}%'.format(filters[0])),
                models.Interviews.technologies.ilike('%{}%'.format(filters[0])),
                models.Interviews.question_description.ilike('%{}%'.format(filters[0])),
                models.Interviews.tips.ilike('%{}%'.format(filters[0]))
            ),
            # Filter by difficulty rating
            sqlalchemy.or_(
                models.Interviews.difficulty.in_(filters[1]),
                len(filters[1]) == 0
            ),
            # Filter by enjoyment rating
            sqlalchemy.or_(
                models.Interviews.enjoyment.in_(filters[2]),
                len(filters[2]) == 0
            ),
            # Filter by class year
            sqlalchemy.or_(
                models.Interviews.grade.in_(filters[3]),
                len(filters[3]) == 0
            ),
            # Filter by location type
            sqlalchemy.or_(
                models.Interviews.location_type.in_(filters[4]),
                len(filters[4]) == 0
            ),
            # Filter by interview type
            sqlalchemy.or_(
                models.Interviews.type.in_(filters[5]),
                len(filters[5]) == 0
            ),
             # Filter by interview outcome
            sqlalchemy.or_(
                models.Interviews.advanced.in_(filters[6]),
                len(filters[6]) == 0
            ),
            # Filter by final round
            sqlalchemy.or_(
                models.Interviews.final_round.in_(filters[7]),
                len(filters[7]) == 0
            ),
             # Filter by interview duration
            sqlalchemy.or_(
                models.Interviews.duration.in_(filters[8]),
                len(filters[8]) == 0
            ),
             # Filter by how-interview 
            sqlalchemy.or_(
                models.Interviews.how_interview.in_(filters[9]),
                len(filters[9]) == 0
            ),
            # Filter by major
            sqlalchemy.or_(
                models.Interviews.major.in_(filters[10]),
                len(filters[10]) == 0
            ),
            # Filter by certifcates
            sqlalchemy.or_(
                *clauses,
                len(filters[11]) == 0
            ),
            # Filter by job field
            sqlalchemy.or_(
                models.Interviews.job_field.in_(filters[12]),
                len(filters[12]) == 0
            )
        ).order_by(
            *sort_by_clauses
        ).all()
    return interviews

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

# Change interview upvotes
def upvote_interview(id, new_val):
    # Make sure to only get one
    interview = None
    with sqlalchemy.orm.Session(engine) as session:
        interview = session.query(models.Interviews).filter(
            models.Interviews.id == id).update(
                {
                    "upvotes": new_val
                }
            )
        session.commit()
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
        internships = session.query(models.Internships).order_by(
            models.Internships.date_created.desc(),
            sqlalchemy.func.cardinality(models.Internships.upvotes).desc(),
            models.Internships.difficulty.desc(),
            models.Internships.enjoyment.desc()
        ).all()
    return internships

# Get all internship location options
def get_all_internship_locations():
    locations = []
    with sqlalchemy.orm.Session(engine) as session:
        internships = session.query(models.Internships).all()
    for internship in internships:
        if internship.location not in locations:
            locations.append(internship.location)
    return locations

# Get internships by filter
'''
    Filters list is as follows:
    [
        Query, Difficulty List, Enjoyment List, Class Year,
        Location Style, Job Type, Locations, Majors, Certificates,
        Job Fields, Sort By Type, Sort By Direction
    ]
'''
def get_filtered_internships(filters) -> List[models.Internships]:
    internships = []
    clauses = [models.Internships.certificates.contains(elem) for elem in filters[8]]
    # Create sort by clauses
    sort_by_clauses = []
    if filters[10] == "recency" and filters[11]:
        sort_by_clauses.append(models.Internships.date_created.desc())
    elif filters[10] == "recency" and not filters[11]:
        sort_by_clauses.append(models.Internships.date_created)
    if filters[10] == "upvotes" and filters[11]:
        sort_by_clauses.append(sqlalchemy.func.cardinality(models.Internships.upvotes).desc())
    elif filters[10] == "upvotes" and not filters[11]:
        sort_by_clauses.append(sqlalchemy.func.cardinality(models.Internships.upvotes))
    if filters[10] == "difficulty" and filters[11]:
        sort_by_clauses.append(models.Internships.difficulty.desc())
    elif filters[10] == "difficulty" and not filters[11]:
        sort_by_clauses.append(models.Internships.difficulty)
    if filters[10] == "enjoyment" and filters[11]:
        sort_by_clauses.append(models.Internships.enjoyment.desc())
    elif filters[10] == "enjoyment" and not filters[11]:
        sort_by_clauses.append(models.Internships.enjoyment)
    with sqlalchemy.orm.Session(engine) as session:
        internships = session.query(models.Internships).filter(
            # Filter by query in title, description, technology, or company
            sqlalchemy.or_(
                models.Internships.title.ilike('%{}%'.format(filters[0])),
                models.Internships.company.ilike('%{}%'.format(filters[0])),
                models.Internships.technologies.ilike('%{}%'.format(filters[0])),
                models.Internships.description.ilike('%{}%'.format(filters[0])),
            ),
            # Filter by difficulty rating
            sqlalchemy.or_(
                models.Internships.difficulty.in_(filters[1]),
                len(filters[1]) == 0
            ),
            # Filter by enjoyment rating
            sqlalchemy.or_(
                models.Internships.enjoyment.in_(filters[2]),
                len(filters[2]) == 0
            ),
            # Filter by class year
            sqlalchemy.or_(
                models.Internships.grade.in_(filters[3]),
                len(filters[3]) == 0
            ),
            # Filter by location style
            sqlalchemy.or_(
                models.Internships.virtual.in_(filters[4]),
                len(filters[4]) == 0
            ),
            # Filter by job type
            sqlalchemy.or_(
                models.Internships.type.in_(filters[5]),
                len(filters[5]) == 0
            ),
            # Filter by location
            sqlalchemy.or_(
                models.Internships.location.in_(filters[6]),
                len(filters[6]) == 0
            ),
            # Filter by major
            sqlalchemy.or_(
                models.Internships.major.in_(filters[7]),
                len(filters[7]) == 0
            ),
            # Filter by certificates
            sqlalchemy.or_(
                *clauses,
                len(filters[8]) == 0
            ),
            # Filter by job field
            sqlalchemy.or_(
                models.Internships.company_type.in_(filters[9]),
                len(filters[9]) == 0
            ),
        ).order_by(
            *sort_by_clauses
        ).all()
    return internships

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
# Change internship upvotes
def upvote_internship(id, new_val):
    # Make sure to only get one
    internship = None
    with sqlalchemy.orm.Session(engine) as session:
        internship = session.query(models.Internships).filter(
            models.Internships.id == id).update(
                {
                    "upvotes": new_val
                }
            )
        session.commit()
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
                    'internship_enjoyment': company.internship_enjoyment,
                    'locations': company.locations,
                    'fields': company.fields,
                    'majors': company.majors,
                    'interview_grades': company.interview_grades,
                    'internship_grades': company.internship_grades,
                    'advanced': company.advanced,
                    'enjoyed_interview': company.enjoyed_interview,
                    'enjoyed_internship': company.enjoyed_internship,
                    'difficult_interview': company.difficult_interview,
                    'difficult_internship': company.difficult_internship
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

# Get all reviews by company
def get_reviews_by_company(id):
    interviews = []
    with sqlalchemy.orm.Session(engine) as session:
        interviews = session.query(models.Interviews).filter(
            models.Interviews.company_id == id
        ).all()
    internships = []
    with sqlalchemy.orm.Session(engine) as session:
        internships = session.query(models.Internships).filter(
            models.Internships.company_id == id
        ).all()
    return (interviews, internships)

# Get all upvoted reviews by user
def get_upvoted_reviews_by_user(netid):
    interviews = []
    with sqlalchemy.orm.Session(engine) as session:
        interviews = session.query(models.Interviews).filter(
            models.Interviews.upvotes.contains([netid])
        ).all()
    internships = []
    with sqlalchemy.orm.Session(engine) as session:
        internships = session.query(models.Internships).filter(
            models.Internships.upvotes.contains([netid])
        ).all()
    return (interviews, internships)