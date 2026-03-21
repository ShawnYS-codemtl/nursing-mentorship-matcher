from app.database import SessionLocal
from app.models import Mentor, Mentee
from app.services.matching import ExplicitMatcher, run_matching_algorithm, run_flow_matching_v2, run_flow_matching_v1

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

    # for m in locked_matches:
    #     print(m['mentor_name'])

    # print("Remaining Mentors: ")
    # for m in remaining_mentors:
    #     print(m.name)
    

    scored_matches_greedy = run_matching_algorithm(remaining_mentors, remaining_mentees, mentor_capacity_map)

    scored_matches_flow = run_flow_matching_v1(
    remaining_mentors,
    remaining_mentees,
    mentor_capacity_map
    )

    final_matches_greedy = locked_matches + scored_matches_greedy['matches']
    final_matches_flow = locked_matches + scored_matches_flow['matches']


    # print(final_matches)

    

    unmatched_mentees_gr = []
    unmatched_mentors_gr = []
    unmatched_mentees_fl = []
    unmatched_mentors_fl = []

    for mentee in scored_matches_greedy['unmatched_mentees']:
        unmatched_mentees_gr.append(mentee["name"])
    
    for mentor in scored_matches_greedy['unmatched_mentors']:
        unmatched_mentors_gr.append(mentor["name"])

    # for mentee in scored_matches_flow['unmatched_mentees']:
    #     unmatched_mentees_fl.append(mentee["name"])
    
    # for mentor in scored_matches_flow['unmatched_mentors']:
    #     unmatched_mentors_fl.append(mentor["name"])
    
    
    
    # print("Locked matches", len(pretty_locked_matches))
    # print(pretty_locked_matches)

    print("Greedy Matches:", len(final_matches_greedy) )
    print(final_matches_greedy)

    print("Unmatched mentees greedy:", len(unmatched_mentees_gr))
    print(unmatched_mentees_gr)
    print("Unmatched mentors greedy:", len(unmatched_mentors_gr))
    print(unmatched_mentors_gr)

    print("Flow Matches:", len(final_matches_flow) )
    print(final_matches_flow)

    # print("Unmatched mentees:", len(unmatched_mentees_fl))
    # print(unmatched_mentees_fl)
    # print("Unmatched mentors:", len(unmatched_mentors_fl))
    # print(unmatched_mentors_fl)


    

if __name__ == "__main__":
    main()
