from app.models import Mentor, Mentee
from app.services.importing.name_matching import build_index, resolve_names


def build_name_lookup(session, session_id):
    mentors = session.query(Mentor).filter(Mentor.session_id == session_id).all()
    mentees = session.query(Mentee).filter(Mentee.session_id == session_id).all()

    return build_index(mentors), build_index(mentees)


def resolve_preferences(session, session_id):
    """Convert stored name preferences into ID references, scoped to session."""
    mentor_index, mentee_index = build_name_lookup(session, session_id)

    mentors = session.query(Mentor).filter(Mentor.session_id == session_id).all()
    mentees = session.query(Mentee).filter(Mentee.session_id == session_id).all()

    for mentor in mentors:
        if not mentor.preferred_mentee_names:
            continue

        resolved_ids = []

        # One answer can name more than one mentee, and a mentor can list
        # several answers, so flatten both into a single ordered id list.
        for name in mentor.preferred_mentee_names:
            for mentee in resolve_names(name, mentee_index):
                if mentee.id not in resolved_ids:
                    resolved_ids.append(mentee.id)

        mentor.preferred_mentee_ids = resolved_ids

    for mentee in mentees:
        if not mentee.preferred_mentor_name:
            continue

        # The form asks for one mentor; if the answer names several, the
        # first one typed wins.
        matches = resolve_names(mentee.preferred_mentor_name, mentor_index)

        if matches:
            mentee.preferred_mentor_id = matches[0].id
