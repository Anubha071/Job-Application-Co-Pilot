from sqlalchemy import Column, Integer, ForeignKey, Text
from app.database import Base
from sqlalchemy import JSON

class Draft(Base):
    __tablename__ = "drafts"
    
    id = Column (Integer, primary_key=True)
    # BROKEN CODE: referenced table name was singular 'application', but the Application model defines __tablename__ = 'applications'.
    # SQLAlchemy needs the exact target table name for foreign keys.
    application_id = Column(Integer, ForeignKey("applications.id"))
    
    fit_analysis = Column(Text)
    resume_rewrite = Column(Text)
    # BROKEN CODE: legacy database column was once misnamed coveR_letter.
    # The model now uses cover_letter consistently.
    cover_letter = Column(Text)
    interview_pack = Column(Text)
    # BROKEN CODE: JSON column fails on corrupt DB data (StopIteration)
    ats_score = Column(Text)
