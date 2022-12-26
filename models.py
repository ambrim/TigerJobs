import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

# Interviews Review Table
class Interviews (Base):
    __tablename__ = 'interviews'
    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)