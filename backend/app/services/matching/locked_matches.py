from app.models import Match

def get_locked_matches_from_db(db_session, session_id):
    locked_rows = (
        db_session.query(Match)
        .filter(Match.is_locked == True, Match.session_id == session_id)
        .all()
    )

    locked_matches = []

    for m in locked_rows:
        locked_matches.append({
            "mentor_id": m.mentor_id,
            "mentor_name": m.mentor.name if m.mentor else None,
            "mentee_id": m.mentee_id,
            "mentee_name": m.mentee.name if m.mentee else None,
            "score": m.match_score if m.match_score is not None else 100,
            "breakdown": {"locked": True},
            "match_type": "locked_manual" if m.is_manual_override else m.match_type
        })

    return locked_matches

def apply_locked_matches(locked_matches, mentors, mentees):
    matched_mentees = set()
    mentor_capacity = {m.id: m.max_mentees for m in mentors}

    for match in locked_matches:
        mentor_id = match["mentor_id"]
        mentee_id = match["mentee_id"]

        if mentor_id not in mentor_capacity:
            continue  # skip invalid data

        if mentor_capacity[mentor_id] <= 0:
            continue  # prevent negative capacity crash

        matched_mentees.add(mentee_id)
        mentor_capacity[mentor_id] -= 1

    return matched_mentees, mentor_capacity
