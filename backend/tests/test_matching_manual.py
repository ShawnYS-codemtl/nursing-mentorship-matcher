# test_matching_manual.py
"""Quick manual tests for calculate_match_score function."""

from app.models import Mentor, Mentee
from app.services.matching.scoring import calculate_match_score

# Create test mentor and mentee objects (in-memory, no database)
def test_perfect_match():
    """Both mentor and mentee perfectly aligned."""
    mentor = Mentor(
        id=1,
        name="Sarah Chen",
        email="sarah@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["pediatrics", "critical_care", "oncology"],
        languages=["English", "Mandarin"],
        race_ethnicity=["asian"],
        lgbtq_status="no",
        extracurricular_interests=["research", "leadership", "sports_fitness"],
        max_mentees=2,
        preferred_mentee_names=[],
        preferred_mentee_ids = None
    )
    
    mentee = Mentee(
        id=1,
        name="Emma Rodriguez",
        email="emma@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["pediatrics", "critical_care", "oncology"],
        languages_needed=['English', 'Mandarin'],
        race_ethnicity=["asian"],
        lgbtq_status="no",
        extracurricular_interests=["research", "leadership", "sports_fitness"],
        preferred_mentor_name_id=None,
        preferred_mentor_name_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("\n✓ TEST: Perfect Match")
    print(f"  Score: {score}")
    print(f"  Breakdown: {breakdown}")
    assert score > 80, f"Expected score > 80, got {score}"
    print("  PASSED\n")


def test_year_constraint_violation():
    """Mentor and mentee same year - should fail."""
    mentor = Mentor(
        id=2,
        name="James Smith",
        email="james@mail.mcgill.ca",
        program="BSN",
        year_in_program=2,  # Same as mentee
        specialties=["pediatrics"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=2,
        name="Alex Johnson",
        email="alex@mail.mcgill.ca",
        program="BSN",
        year_in_program=2,  # Same as mentor
        specialties=["pediatrics"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Year Constraint Violation")
    print(f"  Score: {score}")
    print(f"  Breakdown: {breakdown}")
    assert score == 0, f"Expected score 0, got {score}"
    assert breakdown['constraints_violated'] == True
    print("  PASSED\n")


def test_language_constraint_violation():
    """Mentee needs Spanish, mentor only speaks English - should fail."""
    mentor = Mentor(
        id=3,
        name="Lisa Wong",
        email="lisa@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["critical_care"],
        languages=["English"],  # Only English
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=3,
        name="Maria Garcia",
        email="maria@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["critical_care"],
        languages_needed=["Spanish"],  # Needs Spanish
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Language Constraint Violation")
    print(f"  Score: {score}")
    print(f"  Breakdown: {breakdown}")
    assert score == 0, f"Expected score 0, got {score}"
    assert breakdown['constraints_violated'] == True
    print("  PASSED\n")


def test_language_constraint_satisfied():
    """Mentee needs Spanish, mentor speaks Spanish - should pass."""
    mentor = Mentor(
        id=4,
        name="Carlos Martinez",
        email="carlos@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["critical_care"],
        languages=["English", "Spanish"],  # Speaks Spanish
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=4,
        name="Isabella Flores",
        email="isabella@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["critical_care"],
        languages_needed=["Spanish"],  # Needs Spanish
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Language Constraint Satisfied")
    print(f"  Score: {score}")
    print(f"  Breakdown: {breakdown}")
    assert score > 0, f"Expected score > 0, got {score}"
    assert breakdown['constraints_violated'] == False
    print("  PASSED\n")


def test_explicit_choice_mentor():
    """Mentor explicitly requested this mentee."""
    mentor = Mentor(
        id=5,
        name="Patricia Brown",
        email="patricia@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["mental_health"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=2,
        preferred_mentee_names=[51]  # Explicitly requested mentee ID 51
    )
    
    mentee = Mentee(
        id=51,
        name="David Lee",
        email="david@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["emergency"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Explicit Choice (Mentor)")
    print(f"  Score: {score}")
    print(f"  Breakdown: {breakdown}")
    assert breakdown['explicit_choice'] == 40, f"Expected explicit choice 40, got {breakdown['explicit_choice']}"
    assert "explicitly requested" in str(breakdown['reasons']).lower()
    print("  PASSED\n")


def test_explicit_choice_mentee():
    """Mentee explicitly requested this mentor."""
    mentor = Mentor(
        id=6,
        name="Michael Johnson",
        email="michael@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["pediatrics"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=52,
        name="Sophie Chen",
        email="sophie@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["pediatrics"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=6  # Explicitly requested mentor ID 6
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Explicit Choice (Mentee)")
    print(f"  Score: {score}")
    print(f"  Breakdown: {breakdown}")
    assert breakdown['explicit_choice'] == 40, f"Expected explicit choice 40, got {breakdown['explicit_choice']}"
    print("  PASSED\n")


def test_program_alignment():
    """Same program - should get program alignment points."""
    mentor = Mentor(
        id=7,
        name="Jennifer Davis",
        email="jennifer@mail.mcgill.ca",
        program="Accelerated BSN",
        year_in_program=2,
        specialties=["critical_care"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=53,
        name="Robert Kim",
        email="robert@mail.mcgill.ca",
        program="Accelerated BSN",  # Same program
        year_in_program=1,
        specialties=["critical_care"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Program Alignment")
    print(f"  Score: {score}")
    print(f"  Program alignment score: {breakdown['program_alignment']}")
    assert breakdown['program_alignment'] == 25, f"Expected program alignment 25, got {breakdown['program_alignment']}"
    print("  PASSED\n")


def test_specialty_alignment():
    """Shared specialties - should get specialty alignment points."""
    mentor = Mentor(
        id=8,
        name="Rachel Foster",
        email="rachel@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["pediatrics", "emergency"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=54,
        name="Thomas Anderson",
        email="thomas@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["pediatrics", "oncology"],  # Shares "pediatrics"
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Specialty Alignment")
    print(f"  Score: {score}")
    print(f"  Specialty alignment score: {breakdown['specialty_alignment']}")
    assert breakdown['specialty_alignment'] > 0, "Expected specialty alignment > 0"
    assert "pediatrics" in str(breakdown['reasons']).lower()
    print("  PASSED\n")


def test_specialty_mismatch():
    """Different specialties - should get penalty."""
    mentor = Mentor(
        id=9,
        name="Oliver White",
        email="oliver@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["geriatrics"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=55,
        name="Natalie Green",
        email="natalie@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["pediatrics"],  # Different specialty
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Specialty Mismatch")
    print(f"  Score: {score}")
    print(f"  Specialty mismatch score: {breakdown['specialty_mismatch']}")
    assert breakdown['specialty_mismatch'] == -5, f"Expected -5 penalty, got {breakdown['specialty_mismatch']}"
    print("  PASSED\n")


def test_identity_match_lgbtq():
    """Both identify as LGBTQ+ - should get identity bonus."""
    mentor = Mentor(
        id=10,
        name="Casey Taylor",
        email="casey@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["mental_health"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="yes",  # LGBTQ+
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=56,
        name="Morgan Scott",
        email="morgan@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["mental_health"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="yes",  # LGBTQ+
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Identity Match (LGBTQ+)")
    print(f"  Score: {score}")
    print(f"  Identity/extracurricular score: {breakdown['identity_extracurricular']}")
    assert breakdown['identity_extracurricular'] > 0, "Expected identity points > 0"
    assert "lgbtq" in str(breakdown['reasons']).lower()
    print("  PASSED\n")


def test_identity_match_firstgen():
    """Both first-gen college - should get identity bonus."""
    mentor = Mentor(
        id=11,
        name="Victoria Lopez",
        email="victoria@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["critical_care"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=57,
        name="Marcus Brown",
        email="marcus@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["critical_care"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=[],
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Identity Match (First-gen College)")
    print(f"  Score: {score}")
    print(f"  Identity/extracurricular score: {breakdown['identity_extracurricular']}")
    assert breakdown['identity_extracurricular'] > 0, "Expected identity points > 0"
    assert "first-generation" in str(breakdown['reasons']).lower()
    print("  PASSED\n")


def test_extracurricular_match():
    """Shared extracurricular interests."""
    mentor = Mentor(
        id=12,
        name="Daniel Hall",
        email="daniel@mail.mcgill.ca",
        program="BSN",
        year_in_program=3,
        specialties=["research"],
        languages=["English"],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=["research", "leadership"],
        max_mentees=1,
        preferred_mentee_names=[]
    )
    
    mentee = Mentee(
        id=58,
        name="Olivia Evans",
        email="olivia@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["research"],
        languages_needed=[],
        race_ethnicity=[],
        lgbtq_status="no",
        extracurricular_interests=["research", "volunteering"],  # Shared "research"
        preferred_mentor_name=None
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Extracurricular Match")
    print(f"  Score: {score}")
    print(f"  Identity/extracurricular score: {breakdown['identity_extracurricular']}")
    assert breakdown['identity_extracurricular'] > 0, "Expected identity points > 0"
    print("  PASSED\n")


def test_score_bounds():
    """Score should never exceed 100."""
    mentor = Mentor(
        id=13,
        name="Sophia Martinez",
        email="sophia@mail.mcgill.ca",
        program="BSN",
        year_in_program=4,
        specialties=["pediatrics"],
        languages=["English"],
        race_ethnicity=["hispanic"],
        lgbtq_status="yes",
        extracurricular_interests=["research"],
        max_mentees=3,
        preferred_mentee_names=[59]
    )
    
    mentee = Mentee(
        id=59,
        name="Lucas Gutierrez",
        email="lucas@mail.mcgill.ca",
        program="BSN",
        year_in_program=1,
        specialties=["pediatrics"],
        languages_needed=[],
        race_ethnicity=["hispanic"],
        lgbtq_status="yes",
        extracurricular_interests=["research"],
        preferred_mentor_name=13
    )
    
    score, breakdown = calculate_match_score(mentor, mentee, debug=True)
    
    print("✓ TEST: Score Bounds")
    print(f"  Score: {score}")
    assert 0 <= score <= 100, f"Expected score between 0-100, got {score}"
    print("  PASSED\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING calculate_match_score FUNCTION")
    print("="*60)
    
    # test_perfect_match()
    # test_year_constraint_violation()
    test_language_constraint_violation()
    # test_language_constraint_satisfied()
    # test_explicit_choice_mentor()
    # test_explicit_choice_mentee()
    # test_program_alignment()
    # test_specialty_alignment()
    # test_specialty_mismatch()
    # test_identity_match_lgbtq()
    # test_identity_match_firstgen()
    # test_extracurricular_match()
    # test_score_bounds()
    
    print("="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60 + "\n")