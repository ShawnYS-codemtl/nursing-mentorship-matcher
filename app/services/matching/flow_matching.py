import networkx as nx
from app.services.matching.scoring import calculate_match_score


def run_flow_matching_v1(valid_mentors, valid_mentees, mentor_capacity_map):
    G = nx.DiGraph()

    SOURCE = "source"
    SINK = "sink"

    # -------------------------
    # Step 1: Source → Mentors
    # -------------------------
    for mentor in valid_mentors:
        capacity = mentor_capacity_map.get(mentor.id, 0)
        
        if capacity <= 0: 
            print("Mentor name, id: " + mentor.name + ", " + str(mentor.id))
        if capacity > 0:
            G.add_edge(SOURCE, f"mentor_{mentor.id}", capacity=capacity, weight=0)

    # -------------------------
    # Step 2: Mentors → Mentees
    # -------------------------
    for mentor in valid_mentors:
        if mentor_capacity_map.get(mentor.id, 0) <= 0:
            continue

        for mentee in valid_mentees:
            score, breakdown = calculate_match_score(mentor, mentee)

            # Keep same inclusion logic as before
            if score > 0:
                G.add_edge(
                    f"mentor_{mentor.id}",
                    f"mentee_{mentee.id}",
                    capacity=1,
                    weight=-score  # maximize score
                )

    # -------------------------
    # Step 3: Mentees → Sink
    # -------------------------
    for mentee in valid_mentees:
        G.add_edge(f"mentee_{mentee.id}", SINK, capacity=1, weight=0)

    # -------------------------
    # Step 4: Solve flow
    # -------------------------
    flow_dict = nx.max_flow_min_cost(G, SOURCE, SINK)

    # -------------------------
    # Step 5: Extract matches
    # -------------------------
    matches = []
    pretty_matches = []

    mentor_lookup = {m.id: m for m in valid_mentors}
    mentee_lookup = {m.id: m for m in valid_mentees}

    for mentor in valid_mentors:
        mentor_node = f"mentor_{mentor.id}"

        for mentee_node, flow in flow_dict.get(mentor_node, {}).items():
            if flow > 0 and mentee_node.startswith("mentee_"):
                mentee_id = int(mentee_node.split("_")[1])
                mentee = mentee_lookup[mentee_id]

                score, breakdown = calculate_match_score(mentor, mentee)

                matches.append({
                    'mentor_id': mentor.id,
                    'mentor_name': mentor.name,
                    'mentee_id': mentee.id,
                    'mentee_name': mentee.name,
                    'score': score,
                    'breakdown': breakdown,
                    'match_type': 'algorithmic'
                })

                pretty_matches.append((mentor.name, mentee.name))  

    # -------------------------
    # Step 6: Unmatched
    # -------------------------
    matched_mentee_ids = {m['mentee_id'] for m in matches}
    matched_mentor_ids = {m['mentor_id'] for m in matches}

    unmatched_mentees = [
        {
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'reason': 'No compatible mentors available'
        }
        for m in valid_mentees
        if m.id not in matched_mentee_ids
    ]

    unmatched_mentors = []

    for mentor in valid_mentors:
        node = f"mentor_{mentor.id}"
        capacity = mentor_capacity_map.get(mentor.id, 0)

        used = flow_dict.get(SOURCE, {}).get(node, 0)

        remaining = capacity - used

        if remaining > 0:
            unmatched_mentors.append({
                'id': mentor.id,
                'name': mentor.name,
                'email': mentor.email,
                'reason': f'Capacity remaining: {remaining}'
            })

    total_used = sum(flow_dict[SOURCE].values())
    print("Total flow:", total_used)
    total_remaining = sum(
    mentor_capacity_map[m.id] - flow_dict.get(SOURCE, {}).get(f"mentor_{m.id}", 0)
    for m in valid_mentors
    )

    print("Total capacity:", total_used + total_remaining)

    return {
        'matches': matches,
        'pretty_matches': pretty_matches,
        'unmatched_mentees': unmatched_mentees,
        'unmatched_mentors': unmatched_mentors,
        'statistics': {
            'total_mentors': len(valid_mentors),
            'total_mentees': len(valid_mentees),
            'matched_pairs': len(matches),
            'unmatched_mentees': len(unmatched_mentees),
            'unmatched_mentors': len(unmatched_mentors),
            'average_match_score': sum(m['score'] for m in matches) / len(matches) if matches else 0,
        }
    }

def run_flow_matching_v2(valid_mentors, valid_mentees, mentor_capacity_map):
    G = nx.DiGraph()

    SOURCE = "source"
    SINK = "sink"

    BIG_CONSTANT = 1000  # must be >> max possible score (your max ~100)

    # -------------------------
    # Step 1: Source → Mentors
    # -------------------------
    for mentor in valid_mentors:
        capacity = mentor_capacity_map.get(mentor.id, 0)
        if capacity > 0:
            G.add_edge(SOURCE, f"mentor_{mentor.id}", capacity=capacity, weight=0)

    # -------------------------
    # Step 2: Mentors → Mentees
    # -------------------------
    for mentor in valid_mentors:
        if mentor_capacity_map.get(mentor.id, 0) <= 0:
            continue

        for mentee in valid_mentees:
            score, breakdown = calculate_match_score(mentor, mentee)

        # ❌ HARD FILTER
        if breakdown['constraints_violated']:
            continue

        if breakdown['explicit_choice'] > 0:
            adjusted_score = score + 1000  # force explicit matches
        else:
            if score >= 20:
                adjusted_score = score
            else:
                adjusted_score = score - 10  # light penalty only

        G.add_edge(
            f"mentor_{mentor.id}",
            f"mentee_{mentee.id}",
            capacity=1,
            weight=-adjusted_score
        )

    # -------------------------
    # Step 3: Mentees → Sink
    # -------------------------
    UNMATCHED_PENALTY = 200

    for mentee in valid_mentees:
        G.add_edge(
            f"mentee_{mentee.id}",
            SINK,
            capacity=1,
            weight=UNMATCHED_PENALTY
        )

    # -------------------------
    # Step 4: Solve flow
    # -------------------------
    flow_dict = nx.max_flow_min_cost(G, SOURCE, SINK)

    # -------------------------
    # Step 5: Extract matches
    # -------------------------
    matches = []
    pretty_matches = []

    mentor_lookup = {m.id: m for m in valid_mentors}
    mentee_lookup = {m.id: m for m in valid_mentees}

    for mentor in valid_mentors:
        mentor_node = f"mentor_{mentor.id}"

        if mentor_node not in flow_dict:
            continue

        for mentee_node, flow in flow_dict[mentor_node].items():
            if flow > 0 and mentee_node.startswith("mentee_"):
                mentee_id = int(mentee_node.split("_")[1])
                mentee = mentee_lookup[mentee_id]

                score, breakdown = calculate_match_score(mentor, mentee)

                matches.append({
                    'mentor_id': mentor.id,
                    'mentor_name': mentor.name,
                    'mentee_id': mentee.id,
                    'mentee_name': mentee.name,
                    'score': score,
                    'breakdown': breakdown,
                    'match_type': 'algorithmic'
                })

                pretty_matches.append((mentor.name, mentee.name))

                mentor_capacity_map[mentor.id] -= 1

    # -------------------------
    # Step 6: Unmatched
    # -------------------------
    matched_mentee_ids = {m['mentee_id'] for m in matches}
    matched_mentor_ids = {m['mentor_id'] for m in matches}

    unmatched_mentees = [
        {
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'reason': 'No compatible mentors available (score < 20 or no capacity)'
        }
        for m in valid_mentees
        if m.id not in matched_mentee_ids
    ]

    unmatched_mentors = [
        {
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'reason': f'Capacity remaining: {mentor_capacity_map.get(m.id, 0)}'
        }
        for m in valid_mentors
        if mentor_capacity_map.get(m.id, 0) > 0
    ]

    return {
        'matches': matches,
        'pretty_matches': pretty_matches,
        'unmatched_mentees': unmatched_mentees,
        'unmatched_mentors': unmatched_mentors,
        'statistics': {
            'total_mentors': len(valid_mentors),
            'total_mentees': len(valid_mentees),
            'matched_pairs': len(matches),
            'unmatched_mentees': len(unmatched_mentees),
            'unmatched_mentors': len(unmatched_mentors),
            'average_match_score': sum(m['score'] for m in matches) / len(matches) if matches else 0,
        }
    }