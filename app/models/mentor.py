from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone

class Mentor(Base):
    __tablename__ = 'mentors'
    id = Column(Integer, primary_key=True)
    form_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    program = Column(String, nullable=False) # 'BSN', 'Accelerated BSN', 'RN-to-BSN'
    year_in_program = Column(Integer, nullable=False)
    specialties = Column(JSON, default=[])
    languages = Column(JSON, default=["English"])
    race_ethnicity = Column(JSON, default=[])
    lgbtq_status = Column(String)
    extracurricular_interests = Column(JSON, default=[])
    max_mentees = Column(Integer, nullable=False)
    preferred_mentees = Column(JSON, default=[]) # List of mentee names
    data_cycle = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    matches = relationship("Match", foreign_keys="Match.mentor_id", back_populates="mentor")
