from flask import Blueprint, jsonify
from app.database import Base, engine
from app.models.mentor import Mentor  # noqa: F401 — must be imported to register with Base
from app.models.mentee import Mentee  # noqa: F401
from app.models.match import Match    # noqa: F401
import traceback

reset_bp = Blueprint("reset", __name__)

@reset_bp.route("/reset-db", methods=["POST"])
def reset_db():
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        return jsonify({"status": "success", "message": "Database reset complete"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
