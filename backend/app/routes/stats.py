from flask import Blueprint, jsonify
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Mentor, Mentee, Match
from app.utils.session import require_session_id

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    session_id, err = require_session_id()
    if err:
        return err

    session = SessionLocal()

    try:
        mentor_count = session.query(func.count(Mentor.id)).filter(Mentor.session_id == session_id).scalar()
        mentee_count = session.query(func.count(Mentee.id)).filter(Mentee.session_id == session_id).scalar()
        match_count = session.query(func.count(Match.id)).filter(Match.session_id == session_id).scalar()

        # Unmatched mentees (within session)
        matched_mentee_ids = (
            session.query(Match.mentee_id)
            .filter(Match.session_id == session_id)
            .subquery()
        )

        unmatched_mentees = (
            session.query(func.count(Mentee.id))
            .filter(Mentee.session_id == session_id, ~Mentee.id.in_(matched_mentee_ids))
            .scalar()
        )

        # Available mentors by capacity (within session)
        mentor_match_counts = (
            session.query(
                Match.mentor_id,
                func.count(Match.id).label("match_count")
            )
            .filter(Match.session_id == session_id)
            .group_by(Match.mentor_id)
            .subquery()
        )

        available_mentors = (
            session.query(func.count(Mentor.id))
            .filter(Mentor.session_id == session_id)
            .outerjoin(
                mentor_match_counts,
                Mentor.id == mentor_match_counts.c.mentor_id
            )
            .filter(
                (Mentor.max_mentees - func.coalesce(mentor_match_counts.c.match_count, 0)) > 0
            )
            .scalar()
        )

        # Score stats (within session)
        avg_score = session.query(func.avg(Match.match_score)).filter(Match.session_id == session_id).scalar()
        min_score = session.query(func.min(Match.match_score)).filter(Match.session_id == session_id).scalar()
        max_score = session.query(func.max(Match.match_score)).filter(Match.session_id == session_id).scalar()

        scores = (
            session.query(Match.match_score)
            .filter(Match.session_id == session_id)
            .order_by(Match.match_score)
            .all()
        )
        scores = [s[0] for s in scores]

        median_score = None
        if scores:
            n = len(scores)
            mid = n // 2
            if n % 2 == 0:
                median_score = (scores[mid - 1] + scores[mid]) / 2
            else:
                median_score = scores[mid]

        return jsonify({
            "mentors": mentor_count,
            "mentees": mentee_count,
            "matches": match_count,
            "unmatched_mentees": unmatched_mentees,
            "available_mentors": available_mentors,
            "avg_score": round(avg_score, 2) if avg_score else None,
            "min_score": min_score,
            "max_score": max_score,
            "median_score": median_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()
