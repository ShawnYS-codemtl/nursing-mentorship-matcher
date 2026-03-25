from app.database import SessionLocal
from app.models import Match

def run_matching_and_persist(matching_results):
    session = SessionLocal()

    try:
        # Optional: clear previous matches (important decision)
        # later: only overwrite non-locked matches
        session.query(Match).delete()

        for result in matching_results:
            match = Match(
                mentor_id=result["mentor_id"],
                mentee_id=result["mentee_id"],
                match_score=result["score"],
                match_reason=result.get("breakdown"),
                match_type=result.get("match_type"),
                is_manual_override=False,
                is_locked=False
            )
            session.add(match)

        session.commit()

        return len(matching_results)

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()