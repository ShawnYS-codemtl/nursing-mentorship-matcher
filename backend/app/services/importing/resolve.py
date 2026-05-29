from app.models import Mentor, Mentee

def normalize(name: str):
    if not name:
        return None
    return name.strip().lower().replace(' ', '_')

def build_name_lookup(session, session_id):
    mentors = session.query(Mentor).filter(Mentor.session_id == session_id).all()
    mentees = session.query(Mentee).filter(Mentee.session_id == session_id).all()

    mentor_lookup = {normalize(m.name): m for m in mentors}
    mentee_lookup = {normalize(m.name): m for m in mentees}

    return mentor_lookup, mentee_lookup

def resolve_preferences(session, session_id):
    """Convert stored name preferences into ID references, scoped to session."""
    mentor_lookup, mentee_lookup = build_name_lookup(session, session_id)

    mentors = session.query(Mentor).filter(Mentor.session_id == session_id).all()
    mentees = session.query(Mentee).filter(Mentee.session_id == session_id).all()

    for mentor in mentors:
        if not mentor.preferred_mentee_names:
            continue

        resolved_ids = []
        for name in mentor.preferred_mentee_names:
            mentee = mentee_lookup.get(normalize(name))
            if mentee:
                resolved_ids.append(mentee.id)

        mentor.preferred_mentee_ids = resolved_ids

    for mentee in mentees:
        if not mentee.preferred_mentor_name:
            continue

        mentor = mentor_lookup.get(normalize(mentee.preferred_mentor_name))
        if mentor:
            mentee.preferred_mentor_id = mentor.id
