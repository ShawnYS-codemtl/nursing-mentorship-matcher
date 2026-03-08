from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey('mentors.id'), nullable=False)
    mentee_id = Column(Integer, ForeignKey('mentees.id'), nullable=False)
    match_score = Column(Float, nullable=False)
    match_reason = Column(JSON) # Breakdown of match factors
    explicit_match = Column(Boolean, default=False)
    program_match = Column(Boolean, default=False)
    specialty_match = Column(Boolean, default=False)
    identity_match = Column(Boolean, default=False)
    data_cycle = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    mentor = relationship("Mentor", foreign_keys=[mentor_id], back_populates="matches")
    mentee = relationship("Mentee", foreign_keys=[mentee_id], back_populates="match")
