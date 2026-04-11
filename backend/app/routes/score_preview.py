from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Mentee, Mentor
from app.services.matching.scoring import calculate_match_score


match_score_bp = Blueprint("match-score", __name__)

@match_score_bp.route("/match-score", methods=["POST"])
def match_score():
    session = SessionLocal()

    data = request.json

    mentee_id = data.get("mentee_id")
    mentor_id = data.get("mentor_id")

    mentee = session.query(Mentee).filter(Mentee.id == mentee_id).first()
    mentor = session.query(Mentor).filter(Mentor.id == mentor_id).first()

    score, breakdown = calculate_match_score(mentor, mentee)

    return {
        "score": score,
        "breakdown": breakdown
    }