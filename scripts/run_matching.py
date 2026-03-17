from app.database import SessionLocal
from app.models import Mentor, Mentee
from app.services.matching import ExplicitMatcher, run_matching_algorithm

def main():
    session = SessionLocal()

    mentors = session.query(Mentor).all()
    mentees = session.query(Mentee).all()

    matcher = ExplicitMatcher(mentors, mentees)
    locked_matches, (remaining_mentors, remaining_mentees), pretty_locked_matches, mentor_capacity_map = matcher.run()

    # print("Mentors length:", len(mentors))
    # print("Remaining mentors length:", len(remaining_mentors))
    # print("Mentees length:", len(mentees))
    # print("Remaining mentees length:", len(remaining_mentees))

    scored = run_matching_algorithm(remaining_mentors, remaining_mentees, mentor_capacity_map)

    final_matches = locked_matches + scored['matches']

    # print(final_matches)

    

    unmatched_mentees = []
    unmatched_mentors = []

    for mentee in scored['unmatched_mentees']:
        unmatched_mentees.append(mentee["name"])
    
    for mentor in scored['unmatched_mentors']:
        unmatched_mentors.append(mentor["name"])
    
    print("Locked matches", len(pretty_locked_matches))
    print(pretty_locked_matches)
    print("Matches:", len(scored["pretty_matches"]) )
    print(scored["pretty_matches"])
    print("Unmatched mentees:", len(unmatched_mentees))
    print(unmatched_mentees)
    print("Unmatched mentors:", len(unmatched_mentors))
    print(unmatched_mentors)

if __name__ == "__main__":
    main()
