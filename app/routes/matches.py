from flask import Blueprint, jsonify
from app.database import SessionLocal
from app.models import Match
from sqlalchemy.orm import joinedload

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