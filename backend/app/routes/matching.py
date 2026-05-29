from flask import Blueprint, jsonify, request
from app.services.matching.persist_matches import run_matching_and_persist
from app.services.matching.flow_matching import run_flow_matching_v1
from app.database import SessionLocal
from app.models import Mentor, Mentee
from app.services.matching.explicit_matcher import ExplicitMatcher
from app.services.matching.locked_matches import get_locked_matches_from_db, apply_locked_matches
from app.utils.session import require_session_id
import traceback

matching_bp = Blueprint("matching", __name__)

@matching_bp.route("/run-matching", methods=["POST"])
def run_matching():
    session_id, err = require_session_id()
    if err:
        return err

    session = SessionLocal()

    try:
        mentors = session.query(Mentor).filter(Mentor.session_id == session_id).all()
        mentees = session.query(Mentee).filter(Mentee.session_id == session_id).all()

        locked_matches = get_locked_matches_from_db(session, session_id)
        matched_mentees, mentor_capacity = apply_locked_matches(locked_matches, mentors, mentees)

        matcher = ExplicitMatcher(mentors, mentees, pre_matched_mentees=matched_mentees, mentor_capacity=mentor_capacity)
        explicit_matches, (remaining_mentors, remaining_mentees), pretty_explicit_matches, mentor_capacity_map = matcher.run()
        scored_matches = run_flow_matching_v1(remaining_mentors, remaining_mentees, mentor_capacity_map)
        final_matches_flow = locked_matches + explicit_matches + scored_matches['matches']
        count = run_matching_and_persist(final_matches_flow, session_id)

        return jsonify({
            "status": "success",
            "matches_created": count
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
