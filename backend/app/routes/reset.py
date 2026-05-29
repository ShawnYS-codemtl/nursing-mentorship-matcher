from flask import Blueprint, jsonify
from app.database import SessionLocal
from app.models.mentor import Mentor
from app.models.mentee import Mentee
from app.models.match import Match
from app.utils.session import require_session_id
import traceback

reset_bp = Blueprint("reset", __name__)

@reset_bp.route("/reset-db", methods=["POST"])
def reset_db():
    session_id, err = require_session_id()
    if err:
        return err

    session = SessionLocal()

    try:
        # Delete only this session's data, leaving other sessions untouched
        session.query(Match).filter(Match.session_id == session_id).delete(synchronize_session=False)
        session.query(Mentee).filter(Mentee.session_id == session_id).delete(synchronize_session=False)
        session.query(Mentor).filter(Mentor.session_id == session_id).delete(synchronize_session=False)
        session.commit()
        return jsonify({"status": "success", "message": "Workspace data cleared"})
    except Exception as e:
        session.rollback()
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
