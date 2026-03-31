from app.services.google_sheets import get_mentor_rows, get_mentee_rows
from app.services.form_processors import process_mentor_form_submission, process_mentee_form_submission
# from app.database import SessionLocal

def main():
    # session = SessionLocal()

    rows = get_mentor_rows()
    mentee_rows = get_mentee_rows()

    for row in mentee_rows:
        # mentor = process_mentor_form_submission(row)
        # print("RAW ROW:")
        # print(row)

        # print("\nTRANSFORMED OBJECT:")
        # print(vars(mentor))   # prints the Mentor object's attributes

        # print("\n----------------------\n")
        mentee = process_mentee_form_submission(row)
        print("RAW ROW:")
        print(row)

        print("\nTRANSFORMED OBJECT:")
        print(vars(mentee))

        print("\n----------------------\n")

        # session.add(mentor)

    # session.commit()
    # print("Mentors inserted successfully")
    print("Mentees inserted successfully")
if __name__ == "__main__":
    main()