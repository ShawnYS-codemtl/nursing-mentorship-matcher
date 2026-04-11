from app.database import SessionLocal
from app.models import Match

def run_matching_and_persist(matching_results):
    session = SessionLocal()

    try:
        seen = set()
        deduped_results = []

        for r in matching_results:
            key = (r["mentor_id"], r["mentee_id"])

            if key in seen:
                continue

            seen.add(key)
            deduped_results.append(r)

        # later: only overwrite non-locked matches
        session.query(Match)\
            .filter(Match.is_locked == False)\
            .delete(synchronize_session=False)

        for result in deduped_results:
            match = Match(
                mentor_id=result["mentor_id"],
                mentee_id=result["mentee_id"],
                match_score=result["score"],
                match_reason=result.get("breakdown"),
                match_type=result.get("match_type"),
                is_manual_override=False,
                is_locked=result.get("is_locked", False)
            )
            existing = session.query(Match).filter_by(
                mentor_id=result["mentor_id"],
                mentee_id=result["mentee_id"]
            ).first()

            if existing:
                continue

            session.add(match)

        session.commit()

        return len(seen)

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()