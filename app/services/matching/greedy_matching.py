from app.services.matching.scoring import calculate_match_score
import copy



def run_matching_algorithm(valid_mentors, valid_mentees, mentor_capacity_map):
    """
    Greedy bipartite matching algorithm.
    
    Approach:
    1. Calculate all possible match scores between mentors and mentees
    2. Sort matches by score (descending)
    3. Greedily assign matches in priority order
    4. Track unmatched participants and reasons
    """
    capacity_for_flow = copy.deepcopy(mentor_capacity_map)
    
    # Step 1: Calculate all possible matches with scores
    all_possible_matches = []
    
    for mentor in valid_mentors:
        for mentee in valid_mentees:
            score, breakdown = calculate_match_score(mentor, mentee)
            
            if score > 0 or breakdown['explicit_choice'] > 0:
                # Include even low-scoring matches if explicit choice
                all_possible_matches.append({
                    'mentor': mentor,
                    'mentee': mentee,
                    'score': score,
                    'breakdown': breakdown,
                    'explicit': breakdown['explicit_choice'] > 0
                })
    
    # Step 2: Sort by score (explicit matches first, then by total score)
    # Python's stable sort preserves order for equal scores
    all_possible_matches.sort(
        key=lambda x: (x['explicit'], x['score']),
        reverse=True
    )
    
    # Step 3: Greedy assignment
    matches = []
    pretty_matches = []
    assigned_mentees = set()  # Track matched mentees
    
    for potential_match in all_possible_matches:
        mentor = potential_match['mentor']
        mentee = potential_match['mentee']
        
        # Check constraints
        if mentee.id in assigned_mentees:
            continue  # Mentee already matched
        
        if capacity_for_flow[mentor.id] <= 0:
            continue
        
        # Assign match
        matches.append({
            'mentor_id': mentor.id,
            'mentor_name': mentor.name,
            'mentee_id': mentee.id,
            'mentee_name': mentee.name,
            'score': potential_match['score'],
            'breakdown': potential_match['breakdown'],
            'match_type': 'algorithmic'
        })

        pretty_matches.append((mentor.name, mentee.name))
        
        assigned_mentees.add(mentee.id)
        capacity_for_flow[mentor.id] -= 1
    
    # Step 4: Identify unmatched participants and reasons
    matched_mentee_ids = {m['mentee_id'] for m in matches}
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
    
    matched_mentor_ids = {m['mentor_id'] for m in matches}
    unmatched_mentors = [
        {
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'reason': f'Capacity filled or no compatible mentees (max: {m.max_mentees})'
        }
        for m in valid_mentors
        if m.id not in matched_mentor_ids
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
            'explicit_matches': sum(1 for m in matches if m['breakdown']['explicit_choice'] > 0)
        }
    }