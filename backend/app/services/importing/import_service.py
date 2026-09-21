from app.database import SessionLocal
from app.models import Mentor, Mentee
from app.services.parsing.form_processors import (
    build_mentee_from_row,
    build_mentor_from_row
)
from app.services.importing.resolve import resolve_preferences


def _dedupe_key(email):
    """Emails are case-insensitive in practice; compare them that way."""
    return (email or "").strip().lower()


def _existing_emails(session, model, session_id):
    rows = session.query(model.email).filter(model.session_id == session_id).all()
    return {_dedupe_key(email) for (email,) in rows}


def _insert_new(session, rows, builder, model, session_id):
    """Add one record per unseen email, skipping duplicates already in the DB
    and duplicates repeated within this batch."""
    seen = _existing_emails(session, model, session_id)
    inserted = 0

    for row in rows:
        record = builder(row, session_id)
        key = _dedupe_key(record.email)

        if key in seen:
            continue

        seen.add(key)
        session.add(record)
        inserted += 1

    return inserted


def import_data(get_mentor_rows, get_mentee_rows, session_id):
    session = SessionLocal()

    try:
        mentor_rows = get_mentor_rows()
        mentee_rows = get_mentee_rows()

        inserted_mentees = _insert_new(
            session, mentee_rows, build_mentee_from_row, Mentee, session_id
        )

        inserted_mentors = _insert_new(
            session, mentor_rows, build_mentor_from_row, Mentor, session_id
        )

        session.commit()

        # --- Resolve preferences ---
        resolve_preferences(session, session_id)
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
