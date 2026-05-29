from flask import Blueprint, Response
from io import StringIO
import csv
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.models import Match
from app.utils.session import require_session_id

export_bp = Blueprint("export", __name__)

@export_bp.route("/export", methods=["GET"])
def export_matches():
    session_id, err = require_session_id()
    if err:
        return err

    session = SessionLocal()

    try:
        matches = (
            session.query(Match)
            .filter(Match.session_id == session_id)
            .options(
                joinedload(Match.mentor),
                joinedload(Match.mentee)
            )
            .all()
        )

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "mentor_name",
            "mentor_email",
            "mentee_name",
            "mentee_email",
            "score",
            "match_type",
            "reason_summary"
        ])

        for match in matches:
            reason = match.match_reason or {}
            summary = "; ".join(reason.get("reasons", []))
            writer.writerow([
                match.mentor.name,
                match.mentor.email,
                match.mentee.name,
                match.mentee.email,
                match.match_score,
                match.match_type,
                summary
            ])

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=matches.csv"
            }
        )

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        session.close()
