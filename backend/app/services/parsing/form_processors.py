from app.models import Mentor, Mentee
import uuid


def build_mentor_from_row(row: dict, session_id: str) -> Mentor:
    mentor = Mentor()
    mentor.session_id = session_id
    mentor.form_id = str(uuid.uuid4())
    mentor.name = row.get("name", "")
    mentor.email = row.get("email", "")
    mentor.program = row.get("program", "")
    mentor.year_in_program = row.get("year_in_program", 0)
    mentor.specialties = row.get("specialties", [])
    mentor.languages = row.get("languages", ["English"])
    mentor.extracurricular_interests = row.get("extracurricular_interests", [])
    mentor.race_ethnicity = row.get("race_ethnicity", [])
    mentor.lgbtq_status = row.get("lgbtq_status", "prefer_not_to_answer")
    mentor.max_mentees = row.get("max_mentees", 1)
    mentor.preferred_mentee_names = row.get("preferred_mentees_names", [])
    return mentor


def build_mentee_from_row(row: dict, session_id: str) -> Mentee:
    mentee = Mentee()
    mentee.session_id = session_id
    mentee.form_id = str(uuid.uuid4())
    mentee.name = row.get("name", "")
    mentee.email = row.get("email", "")
    mentee.program = row.get("program", "")
    mentee.year_in_program = row.get("year_in_program", 0)
    mentee.specialties = row.get("specialties", [])
    mentee.languages_needed = row.get("languages_needed", [])
    mentee.extracurricular_interests = row.get("extracurricular_interests", [])
    mentee.race_ethnicity = row.get("race_ethnicity", [])
    mentee.lgbtq_status = row.get("lgbtq_status", "prefer_not_to_answer")
    mentee.preferred_mentor_name = row.get("preferred_mentor_name") or None
    return mentee
