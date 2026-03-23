from app.services.data_sources.google_sheets import GoogleSheetsDataSource
from app.services.data_sources.csv_source import CSVDataSource
from app.services.parsing.form_processors import process_mentor_form_submission, process_mentee_form_submission
from app.database import SessionLocal
from app.models import Mentor, Mentee
import argparse

def normalize(name: str):
    if not name:
        return None
    return name.strip().lower().replace(' ', '_')

def build_name_lookup(session):
    """
    Builds lookup dictionaries for quick name resolution.
    """

    mentors = session.query(Mentor).all()
    mentees = session.query(Mentee).all()

    mentor_lookup = {normalize(m.name): m for m in mentors}
    mentee_lookup = {normalize(m.name): m for m in mentees}

    return mentor_lookup, mentee_lookup

def resolve_preferences(session):
    """
    Convert stored name preferences into ID references.
    """

    mentor_lookup, mentee_lookup = build_name_lookup(session)

    mentors = session.query(Mentor).all()
    mentees = session.query(Mentee).all()

    # Resolve mentor -> mentee preferences
    for mentor in mentors:
        if not mentor.preferred_mentee_names:
            continue

        resolved_ids = []

        for name in mentor.preferred_mentee_names:

            mentee = mentee_lookup.get(normalize(name))

            if mentee:
                resolved_ids.append(mentee.id)

        mentor.preferred_mentee_ids = resolved_ids

    # Resolve mentee -> mentor preference
    for mentee in mentees:
        if not mentee.preferred_mentor_name:
            continue

        mentor = mentor_lookup.get(normalize(mentee.preferred_mentor_name))

        if mentor:
            mentee.preferred_mentor_id = mentor.id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["sheets", "csv"], default="sheets")
    parser.add_argument("--mentor_csv", help="Path to mentor CSV")
    parser.add_argument("--mentee_csv", help="Path to mentee CSV")

    args = parser.parse_args()

    # Select data source
    if args.source == "sheets":
        data_source = GoogleSheetsDataSource()
    else:
        if not args.mentor_csv or not args.mentee_csv:
            raise ValueError("CSV source requires --mentor_csv and --mentee_csv")
        data_source = CSVDataSource(args.mentor_csv, args.mentee_csv)
    session = SessionLocal()

    try:
        mentor_rows = data_source.get_mentor_rows()
        mentee_rows = data_source.get_mentee_rows()
        print(f"Using data source: {args.source}")

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
        
        # Add all users
        session.commit()
        
        # Resolve name preferences to IDs
        resolve_preferences(session)

        session.commit()

        print(f"Inserted {len(mentee_rows)} mentees")
        print(f"Inserted {len(mentor_rows)} mentors")
        print("Resolved explicit preference references")

    except Exception as e:
        session.rollback()
        print("Import failed:", e)

    finally:
        session.close()


if __name__ == "__main__":
    main()