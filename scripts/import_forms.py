from app.services.google_sheets import get_mentor_rows, get_mentee_rows
from app.services.form_processors import process_mentor_form_submission, process_mentee_form_submission
from app.database import SessionLocal
from app.models.mentor import Mentor
from app.models.mentee import Mentee

def main():
    session = SessionLocal()

    try:
        mentor_rows = get_mentor_rows()
        mentee_rows = get_mentee_rows()

        for row in mentee_rows:
            mentee = process_mentee_form_submission(row)
            existing = session.query(Mentee).filter_by(email=mentee.email).first()

            if not existing:
                session.add(mentee)

        for row in mentor_rows:
            mentor = process_mentor_form_submission(row)

            existing = session.query(Mentor).filter_by(email=mentor.email).first()
            if not existing:
                session.add(mentor)

        session.commit()

        print(f"Inserted {len(mentee_rows)} mentees")
        print(f"Inserted {len(mentor_rows)} mentors")

    except Exception as e:
        session.rollback()
        print("Import failed:", e)

    finally:
        session.close()


if __name__ == "__main__":
    main()