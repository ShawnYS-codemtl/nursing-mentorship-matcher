from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone

class Match(Base):
    __tablename__ = 'matches'
    __table_args__ = (
        UniqueConstraint("mentor_id", "mentee_id", name="uq_match_pair"),
    )
    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False, index=True)
    mentor_id = Column(Integer, ForeignKey('mentors.id'), nullable=False)
    mentee_id = Column(Integer, ForeignKey('mentees.id'), nullable=False)
    match_score = Column(Float, nullable=False)
    match_reason = Column(JSON) # Breakdown of match factors
    match_type = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_manual_override = Column(Boolean)
    is_locked = Column (Boolean, default=False)
    mentor = relationship("Mentor", foreign_keys=[mentor_id], back_populates="matches")
    mentee = relationship("Mentee", foreign_keys=[mentee_id], back_populates="match")
