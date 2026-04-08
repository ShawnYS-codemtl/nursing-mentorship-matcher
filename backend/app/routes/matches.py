from flask import Blueprint, jsonify, request
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Match, Mentor, Mentee
from sqlalchemy.orm import joinedload
from app.services.matching.scoring import calculate_match_score

matches_bp = Blueprint("matches", __name__)

@matches_bp.route("/matches", methods=["GET"])
def get_matches():
    session = SessionLocal()

    try:
        matches = (
            session.query(Match)
            .options(
                joinedload(Match.mentor),
                joinedload(Match.mentee)
            )
            .all()
        )

        result = []

        for match in matches:
            result.append({
                "id": match.id,
                "mentor": {
                    "id": match.mentor.id,
                    "name": match.mentor.name,
                    "email": match.mentor.email
                },
                "mentee": {
                    "id": match.mentee.id,
                    "name": match.mentee.name,
                    "email": match.mentee.email
                },
                "score": match.match_score,
                "match_type": match.match_type,
                "is_manual_override": match.is_manual_override,
                "is_locked": match.is_locked,
                "created_at": match.created_at.isoformat(),
                "match_reason": match.match_reason
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@matches_bp.route("/matches/override", methods=["POST"])
def override_match():
    session = SessionLocal()

    try:
        data = request.get_json()

        mentee_id = data.get("mentee_id")
        new_mentor_id = data.get("new_mentor_id")

        if not mentee_id or not new_mentor_id:
            return jsonify({"error": "mentee_id and new_mentor_id required"}), 400

        # --- Fetch entities ---
        mentee = session.query(Mentee).filter(Mentee.id == mentee_id).first()
        mentor = session.query(Mentor).filter(Mentor.id == new_mentor_id).first()

        if not mentee or not mentor:
            return jsonify({"error": "Mentor or Mentee not found"}), 404

        # --- Check if mentee already has a match ---
        existing_match = (
            session.query(Match)
            .filter(Match.mentee_id == mentee_id)
            .first()
        )

        if existing_match:
            if existing_match.is_locked:
                return jsonify({"error": "Match is locked and cannot be overridden"}), 400
            
            # If same mentor → no-op
            if existing_match.mentor_id == new_mentor_id:
                return jsonify({"status": "no change"}), 200

        # --- Check mentor capacity ---
        match_count = (
            session.query(func.count(Match.id))
            .filter(Match.mentor_id == new_mentor_id)
            .scalar()
        )

        mentor = session.query(Mentor).filter(Mentor.id == new_mentor_id).first()

        if not mentor:
            return jsonify({"error": "Mentor not found"}), 404

        if match_count >= mentor.max_mentees:
            return jsonify({"error": "Mentor is at full capacity"}), 400

        score, breakdown = calculate_match_score(mentor, mentee)

        # --- Remove old match AFTER checks ---
        if existing_match:
            session.delete(existing_match)

        # --- Create new match ---
        new_match = Match(
            mentor_id=new_mentor_id,
            mentee_id=mentee_id,
            match_score=score,
            match_reason={"manual_override": True},
            match_type="manual_override",
            is_manual_override=True,
            is_locked=False
        )

        session.add(new_match)
        session.commit()

        # --- Return full object (frontend-ready) ---
        return jsonify({
            "id": new_match.id,
            "mentor": {
                "id": mentor.id,
                "name": mentor.name,
                "email": mentor.email
            },
            "mentor_capacity": {
                "capacity": mentor.max_mentees,
                "current_matches": match_count,
                "remaining_capacity": mentor.max_mentees - match_count
            },
            "mentee": {
                "id": mentee.id,
                "name": mentee.name,
                "email": mentee.email
            },
            "score": new_match.match_score,
            "match_type": new_match.match_type,
            "is_manual_override": new_match.is_manual_override,
            "is_locked": new_match.is_locked,
            "match_reason": new_match.match_reason,
            "created_at": new_match.created_at.isoformat()
        })

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@matches_bp.route("/matches/<int:match_id>", methods=["DELETE"])
def delete_match(match_id):
    session = SessionLocal()

    try:
        match = session.query(Match).filter(Match.id == match_id).first()

        if not match:
            return jsonify({"error": "Match not found"}), 404

        session.delete(match)
        session.commit()

        return jsonify({
            "message": "Match successfully removed",
            "match_id": match_id
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()