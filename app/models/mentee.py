from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone

class Mentee(Base):
    __tablename__ = 'mentees'
    id = Column(Integer, primary_key=True)
    form_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    program = Column(String, nullable=False)
    year_in_program = Column(Integer, nullable=False)
    specialties = Column(JSON, default=[])
    languages_needed = Column(JSON, default=[])
    race_ethnicity = Column(JSON, default=[])
    lgbtq_status = Column(String)
    extracurricular_interests = Column(JSON, default=[])
    preferred_mentor_id = Column(Integer) # Mentor ID if requested
    data_cycle = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    match = relationship("Match", uselist=False, foreign_keys="Match.mentee_id", back_populates="mentee")
