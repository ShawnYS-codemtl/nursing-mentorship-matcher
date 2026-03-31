from flask import Blueprint, jsonify
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Mentor, Mentee, Match

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    session = SessionLocal()

    try:
        # Total counts
        mentor_count = session.query(func.count(Mentor.id)).scalar()
        mentee_count = session.query(func.count(Mentee.id)).scalar()
        match_count = session.query(func.count(Match.id)).scalar()

        # Unmatched mentees
        matched_mentee_ids = session.query(Match.mentee_id).subquery()

        unmatched_mentees = (
            session.query(func.count(Mentee.id))
            .filter(~Mentee.id.in_(matched_mentee_ids))
            .scalar()
        )

        # Available mentors (based on capacity)
        # Count matches per mentor
        mentor_match_counts = (
            session.query(
                Match.mentor_id,
                func.count(Match.id).label("match_count")
            )
            .group_by(Match.mentor_id)
            .subquery()
        )

        # Join with mentors
        available_mentors = (
            session.query(func.count(Mentor.id))
            .outerjoin(
                mentor_match_counts,
                Mentor.id == mentor_match_counts.c.mentor_id
            )
            .filter(
                (Mentor.max_mentees - func.coalesce(mentor_match_counts.c.match_count, 0)) > 0
            )
            .scalar()
        )

                # --- Score stats (SQL) ---
        avg_score = session.query(func.avg(Match.match_score)).scalar()
        min_score = session.query(func.min(Match.match_score)).scalar()
        max_score = session.query(func.max(Match.match_score)).scalar()

        # --- Median (Python fallback) ---
        scores = session.query(Match.match_score).order_by(Match.match_score).all()
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