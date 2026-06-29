from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from app.database import Base

class Application(Base):
    __tablename__ = 'applications' #Name of the table in the database.
    
    id = Column(
        Integer, 
        primary_key=True,
    )
    
    user_id = Column(
        Integer,
        ForeignKey('users.id'), # This creates a foreign key relationship to the users table.
        nullable=False
    )
    
    company_name = Column(
        String
    )
    
    job_title = Column(
        String
    )
    
    status = Column(
        String,
        default='not_applied' # Default status is 'applied'
    )
    
    job_description = Column(
        Text
    )
    
    resume_text = Column(
        Text
    )
    
    resume_filename = Column(
        String 
    )