from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Mentee, Mentor
from app.services.matching.scoring import calculate_match_score
from app.utils.session import require_session_id


match_score_bp = Blueprint("match-score", __name__)

@match_score_bp.route("/match-score", methods=["POST"])
def match_score():
    session_id, err = require_session_id()
    if err:
        return err

    session = SessionLocal()

    data = request.json

    mentee_id = data.get("mentee_id")
    mentor_id = data.get("mentor_id")

    mentee = session.query(Mentee).filter(Mentee.id == mentee_id, Mentee.session_id == session_id).first()
    mentor = session.query(Mentor).filter(Mentor.id == mentor_id, Mentor.session_id == session_id).first()

    if not mentee or not mentor:
        return jsonify({"error": "Mentor or Mentee not found"}), 404

    score, breakdown = calculate_match_score(mentor, mentee)

    return {
        "score": score,
        "breakdown": breakdown
    }
