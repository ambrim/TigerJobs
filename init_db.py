# File to reset database when needed
import sqlalchemy
import sqlalchemy.orm
import models
import os

db_url = os.getenv("DATABASE_URL")

# Add test users
def add_test_interview(session):
    interview = models.Interviews(
        title="Test"
    )
    session.add(interview)

def main():
    # Create engine and drop and recreate all tables
    engine = sqlalchemy.create_engine(db_url)
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

    with sqlalchemy.orm.Session(engine) as session:
        # Add fake test data if needed
        add_test_interview(session)
        session.commit()
        
    engine.dispose()

if __name__ == '__main__':
    main()


