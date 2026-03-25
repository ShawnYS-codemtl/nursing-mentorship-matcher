from flask import Blueprint, jsonify
from app.services.matching.persist_matches import run_matching_and_persist
from app.services.matching.flow_matching import run_flow_matching_v1
from app.database import SessionLocal
from app.models import Mentor, Mentee
from app.services.matching.explicit_matcher import ExplicitMatcher

matching_bp = Blueprint("matching", __name__)

@matching_bp.route("/run-matching", methods=["POST"])
def run_matching():
    session = SessionLocal()

    try:
        mentors = session.query(Mentor).all()
        mentees = session.query(Mentee).all()

        matcher = ExplicitMatcher(mentors, mentees)
        locked_matches, (remaining_mentors, remaining_mentees), pretty_locked_matches, mentor_capacity_map = matcher.run()
        scored_matches = run_flow_matching_v1(remaining_mentors, remaining_mentees, mentor_capacity_map)
        final_matches_flow = locked_matches + scored_matches['matches']
        count = run_matching_and_persist(final_matches_flow)

        return jsonify({
            "status": "success",
            "matches_created": count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500