from app.database import SessionLocal
from app.models import Mentor, Mentee
from app.services.parsing.form_processors import (
    process_mentor_form_submission,
    process_mentee_form_submission
)
from app.services.importing.resolve import resolve_preferences


def import_data(get_mentor_rows, get_mentee_rows):
    session = SessionLocal()

    try:
        mentor_rows = get_mentor_rows()
        mentee_rows = get_mentee_rows()

        inserted_mentors = 0
        inserted_mentees = 0

        # --- Insert mentees ---
        for row in mentee_rows:
            mentee = process_mentee_form_submission(row)

            existing = session.query(Mentee).filter_by(email=mentee.email).first()
            if not existing:
                session.add(mentee)
                inserted_mentees += 1

        # --- Insert mentors ---
        for row in mentor_rows:
            mentor = process_mentor_form_submission(row)

            existing = session.query(Mentor).filter_by(email=mentor.email).first()
            if not existing:
                session.add(mentor)
                inserted_mentors += 1

        session.commit()

        # --- Resolve preferences ---
        resolve_preferences(session)
        session.commit()

        return {
            "mentors_inserted": inserted_mentors,
            "mentees_inserted": inserted_mentees,
            "total_mentor_rows": len(mentor_rows),
            "total_mentee_rows": len(mentee_rows)
        }

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()