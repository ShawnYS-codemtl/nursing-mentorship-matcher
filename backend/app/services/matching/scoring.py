import logging

logger = logging.getLogger(__name__)

def safe_get_list(value, default=None):
    """Safely convert value to list."""
    if value is None:
        return default or []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [value] if value.strip() else []
    return []

def format_reasons(reasons_list):
    """Format reasons for consistent output."""
    formatted = []
    for reason in reasons_list:
        if reason and reason[0].islower():
            reason = reason[0].upper() + reason[1:]
        formatted.append(reason)
    return formatted

def calculate_match_score(mentor, mentee, weights=None, debug=False):
    """
    Calculate comprehensive match score (0-100).
    
    Weights:
    - Explicit choice: 0 points
    - Program alignment: 35 points
    - Specialty alignment: 35 points
    - Identity/extracurricular: 30 points
    
    Args:
        mentor: Mentor object
        mentee: Mentee object
        weights: Dict of scoring weights (optional)
        debug: If True, log detailed scoring
    
    Returns:
        tuple: (total_score, score_breakdown_dict)
    """
    
    if weights is None:
        weights = {
            'explicit': 0,
            'program': 35,
            'specialty': 35,
            'identity': 30
        }
    
    if debug:
        logger.debug(f"Calculating match: {mentor.name} → {mentee.name}")
    
    score_breakdown = {
        'explicit_choice': False,
        'program_alignment': 0,
        'specialty_alignment': 0,
        'identity_extracurricular': 0,
        'specialty_mismatch': 0,
        'constraints_violated': False,
        'reasons': []
    }
    
    # ==================== HARD CONSTRAINTS ====================
    
    # CONSTRAINT 1: Year requirement
    mentor_year = mentor.year_in_program
    mentee_year = mentee.year_in_program
    
    if mentor_year <= mentee_year:  # Mentor must be strictly ahead
        score_breakdown['constraints_violated'] = True
        score_breakdown['reasons'].append(
            f"Year constraint violated: Mentor is {mentor_year}, "
            f"mentee is {mentee_year} (need mentor to be ahead)"
        )
        if debug:
            logger.debug(f"  ✗ Year constraint failed: {mentor_year} <= {mentee_year}")
        return 0, score_breakdown
    
    # CONSTRAINT 2: Language compatibility
    mentor_languages = set(
        lang.lower().strip() for lang in safe_get_list(mentor.languages, ['english'])
    )
    mentee_required_languages = set(
        lang.lower().strip() for lang in safe_get_list(mentee.languages_needed)
    )

    # At least one language must match
    if mentee_required_languages:
        shared_languages = mentor_languages & mentee_required_languages
        
        if not shared_languages:
            # Mentee needs languages but mentor doesn't speak any of them
            score_breakdown['constraints_violated'] = True
            score_breakdown['reasons'].append(
                f"Language constraint: Mentee needs {mentee.languages_needed}, "
                f"mentor speaks {mentor.languages}"
            )
            if debug:
                logger.debug(f"  ✗ Language constraint failed: no shared languages")
            return 0, score_breakdown

    if debug:
        logger.debug(f"  ✓ All constraints passed")
    
    # ==================== SCORING COMPONENTS ====================
    
    # COMPONENT 1: Explicit choice (highest priority)
    # mentor_preferred_ids = safe_get_list(mentor.preferred_mentee_ids)
    
    # if mentee.id in mentor_preferred_ids:
    #     score_breakdown['explicit_choice'] = weights['explicit']
    #     score_breakdown['reasons'].append("Mentor explicitly requested this mentee")
    #     if debug:
    #         logger.debug(f"  + Explicit choice (mentor): {weights['explicit']} pts")
    # elif mentee.preferred_mentor_id == mentor.id:
    #     score_breakdown['explicit_choice'] = weights['explicit']
    #     score_breakdown['reasons'].append("Mentee explicitly requested this mentor")
    #     if debug:
    #         logger.debug(f"  + Explicit choice (mentee): {weights['explicit']} pts")
    
    # COMPONENT 2: Program alignment
    mentor_program = mentor.program.lower().strip()
    mentee_program = mentee.program.lower().strip()
    
    if mentor_program == mentee_program:
        score_breakdown['program_alignment'] = weights['program']
        score_breakdown['reasons'].append(f"Program match: Both in {mentor.program}")
        if debug:
            logger.debug(f"  + Program match: {weights['program']} pts")
    else:
        # Partial credit for related programs
        related_programs = {
            'BSc(N)': ['BNI Online', 'BNI On Campus'],
            'BNI Online': ['BSc(N)', 'BNI On Campus'],
            'BNI On Campus': ['BNI Online', 'BSc(N)'],
            'MScA in Nursing (Direct Entry)': ['MScA in Advanced Nursing (Nurse Entry)', 'MScA in Nurse Practitioner'],
            'MScA in Advanced Nursing (Nurse Entry)': ['MScA in Nursing (Direct Entry)', 'MScA in Nurse Practitioner'],
            'MScA in Nurse Practitioner': ['MScA in Nursing (Direct Entry)', 'MScA in Advanced Nursing (Nurse Entry)'],
        }
        
        if mentee_program in related_programs.get(mentor_program, []):
            score_breakdown['program_alignment'] = weights['program'] * 0.5
            score_breakdown['reasons'].append(f"Related programs: {mentor.program} and {mentee.program}")
            if debug:
                logger.debug(f"  + Related program match: {weights['program'] * 0.5} pts")
    
    # COMPONENT 3: Specialty alignment
    mentor_specialties = set(
        s.lower().strip() for s in safe_get_list(mentor.specialties)
    )
    mentee_specialties = set(
        s.lower().strip() for s in safe_get_list(mentee.specialties)
    )
    
    shared_specialties = mentor_specialties & mentee_specialties
    
    if shared_specialties:
        # Award full points for any shared specialty
        score_breakdown['specialty_alignment'] = weights['specialty']
        
        # Bonus for strong overlap (2+ shared specialties)
        if len(shared_specialties) >= 2:
            overlap_bonus = (len(shared_specialties) - 1) * 4
            score_breakdown['specialty_alignment'] = min(
                score_breakdown['specialty_alignment'] + overlap_bonus,
                weights['specialty'] * 1.5
            )
        
        score_breakdown['reasons'].append(
            f"Specialty match: {', '.join(sorted(shared_specialties))}"
        )
        if debug:
            logger.debug(f"  + Specialty match: {score_breakdown['specialty_alignment']} pts")
            
    elif mentee_specialties and mentor_specialties:
        # Both have interests, but no overlap
        score_breakdown['specialty_mismatch'] = -5
        score_breakdown['reasons'].append(
            f"Specialty mismatch: mentor interested in {sorted(mentor_specialties)}, "
            f"mentee interested in {sorted(mentee_specialties)}"
        )
        if debug:
            logger.debug(f"  - Specialty mismatch: -5 pts")
            
    # elif not mentee_specialties:
    #     # Mentee hasn't decided yet
    #     score_breakdown['reasons'].append("Mentee still exploring specialties")
    #     if debug:
    #         logger.debug(f"  ~ Mentee still exploring")
    
    # COMPONENT 4: Identity & Extracurricular
    identity_score = 0
    identity_factors = []

    # Language bonus: extra points for shared non-English/French languages
    # (This incentivizes matching people with less common language skills)
    mentor_languages_set = set(
        lang.lower().strip() for lang in safe_get_list(mentor.languages, ['english'])
    )
    mentee_languages_set = set(
        lang.lower().strip() for lang in safe_get_list(mentee.languages_needed)
    )

    shared_languages = mentor_languages_set & mentee_languages_set

    if shared_languages:
        # Remove English and French to identify "other" languages
        other_languages = shared_languages - {'english', 'french'}
        
        if other_languages:
            # Bonus for shared non-standard languages (e.g., Mandarin, Spanish, Vietnamese)
            language_bonus = min(len(other_languages) * 6, 12)  # Max 12 points for languages
            identity_score += language_bonus
            identity_factors.append(
                f"Shared heritage language(s): {', '.join(sorted(other_languages))}"
            )
            if debug:
                logger.debug(f"    + Heritage language match: {language_bonus} pts")
        elif len(shared_languages) > 0:
            # They share English/French (still good for Montreal context)
            # But less bonus since most people speak these
            language_bonus = 4
            identity_score += language_bonus
            identity_factors.append(
                f"Shared language(s): {', '.join(sorted(shared_languages))}"
            )
            if debug:
                logger.debug(f"    + Standard language match: {language_bonus} pt")
    
    # Race/ethnicity match
    mentor_ethnicity = set(
        e.lower().strip() for e in safe_get_list(mentor.race_ethnicity)
    )
    mentee_ethnicity = set(
        e.lower().strip() for e in safe_get_list(mentee.race_ethnicity)
    )
    
    shared_ethnicity = mentor_ethnicity & mentee_ethnicity
    if shared_ethnicity and mentor_ethnicity and mentee_ethnicity:
        identity_score += 8
        identity_factors.append(f"Shared identity: {', '.join(sorted(shared_ethnicity))}")
        if debug:
            logger.debug(f"    + Identity match: 8 pts")
    
    # LGBTQ+ status match
    mentor_lgbtq = (mentor.lgbtq_status or "").lower().strip() == 'yes'
    mentee_lgbtq = (mentee.lgbtq_status or "").lower().strip() == 'yes'
    
    if mentor_lgbtq and mentee_lgbtq:
        identity_score += 4
        identity_factors.append("Both identify as LGBTQ+")
        if debug:
            logger.debug(f"    + LGBTQ+ match: 4 pts")
    
    # Extracurricular interests match
    mentor_interests = set(
        i.lower().strip() for i in safe_get_list(mentor.extracurricular_interests)
    )
    mentee_interests = set(
        i.lower().strip() for i in safe_get_list(mentee.extracurricular_interests)
    )
    
    shared_interests = mentor_interests & mentee_interests
    if shared_interests:
        interest_bonus = min(len(shared_interests) * 3, 8)  # Max 8 points
        identity_score += interest_bonus
        identity_factors.append(f"Shared interests: {', '.join(sorted(shared_interests))}")
        if debug:
            logger.debug(f"    + Interest match: {interest_bonus} pts")
    
    score_breakdown['identity_extracurricular'] = min(identity_score, weights['identity'])
    if identity_factors:
        score_breakdown['reasons'].extend(identity_factors)
    
    # ==================== CALCULATE TOTAL ====================
    
    total_score = (
        score_breakdown['explicit_choice'] +
        score_breakdown['program_alignment'] +
        score_breakdown['specialty_alignment'] +
        score_breakdown['identity_extracurricular'] +
        score_breakdown['specialty_mismatch']
    )
    
    # Ensure score is between 0 and 100
    total_score = max(0, min(total_score, 100))
    
    score_breakdown['reasons'] = format_reasons(score_breakdown['reasons'])
    
    if debug:
        logger.debug(f"  TOTAL SCORE: {total_score}")
    
    return total_score, score_breakdown