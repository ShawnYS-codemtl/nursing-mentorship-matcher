from flask import Blueprint, jsonify
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.database import SessionLocal
from app.models import Mentor, Mentee, Match

unmatched_bp = Blueprint("unmatched", __name__)

@unmatched_bp.route("/unmatched", methods=["GET"])
def get_unmatched():
    session = SessionLocal()

    try:
        # --- Unmatched mentees ---
        matched_mentee_ids = session.query(Match.mentee_id).subquery()

        unmatched_mentees = (
            session.query(Mentee)
            .filter(~Mentee.id.in_(matched_mentee_ids))
            .all()
        )

        unmatched_mentees_result = [
            {
                "id": m.id,
                "name": m.name,
                "email": m.email,
                "program": m.program,
                "year_in_program": m.year_in_program,
                "specialties": m.specialties,
                "languages_needed": m.languages_needed,
                "race_ethnicity": m.race_ethnicity, 
                "lgbtq_status": m.lgbtq_status,
                "extracurricular_interests": m.extracurricular_interests
            }
            for m in unmatched_mentees
        ]

        # --- Mentor match counts ---
        mentor_match_counts = (
            session.query(
                Match.mentor_id,
                func.count(Match.id).label("match_count")
            )
            .group_by(Match.mentor_id)
            .subquery()
        )

        # --- Available mentors ---
        mentors = (
            session.query(
                Mentor,
                func.coalesce(mentor_match_counts.c.match_count, 0).label("match_count")
            )
            .outerjoin(
                mentor_match_counts,
                Mentor.id == mentor_match_counts.c.mentor_id
            )
            .all()
        )

        available_mentors_result = []

        for mentor, match_count in mentors:
            remaining_capacity = mentor.max_mentees - match_count

            if remaining_capacity > 0:
                available_mentors_result.append({
                    "id": mentor.id,
                    "name": mentor.name,
                    "email": mentor.email,
                    "capacity": mentor.max_mentees,
                    "current_matches": match_count,
                    "remaining_capacity": remaining_capacity,
                    "program": mentor.program,
                    "year_in_program": mentor.year_in_program,
                    "specialties": mentor.specialties,
                    "languages": mentor.languages,
                    "race_ethnicity": mentor.race_ethnicity, 
                    "lgbtq_status": mentor.lgbtq_status,
                    "extracurricular_interests": mentor.extracurricular_interests
                })
        
        available_mentors_result.sort(
            key=lambda x: x["remaining_capacity"],
            reverse=True
        )

        return jsonify({
            "unmatched_mentees": unmatched_mentees_result,
            "available_mentors": available_mentors_result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()