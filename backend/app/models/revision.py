from sqlalchemy import Column, Integer, ForeignKey, Text
from app.database import Base

class Revision(Base):
    __tablename__ = "revisions"
    
    id = Column(
        Integer,
        primary_key=True
    )
    
    draft_id = Column(
        Integer,
        ForeignKey("drafts.id")
    )
    
    old_text = Column(Text)
    new_text = Column(Text)
    section = Column(Text)