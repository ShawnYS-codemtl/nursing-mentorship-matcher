from app.models import Mentor, Mentee
import uuid
from .column_map import COLUMN_MAP


# Year mapping
YEAR_MAPPING = {
    "U0 (Undergraduate Year 0)": 0,
    "U1 (Undergraduate Year 1)": 1,
    "U2 (Undergraduate Year 2)": 2,
    "U3 (Undergraduate Year 3)": 3,
    "M1 (Masters Year 1)": 4,
    "M2 (Masters Year 2)": 5,
    "Graduated": 6
}

def normalize_option(value):
    return value.strip().lower().replace(' / ', '/').replace(' ', '_')

def parse_checkbox_field(raw_value, normalize=False):
    values = [v.strip() for v in raw_value.split(",") if v.strip()]
    
    if normalize:
        values = [normalize_option(v) for v in values]
    
    return values

def process_mentor_form_submission(row: dict) -> Mentor:
    """
    Convert Google Form row into Mentor database object.
    
    Args:
        row: Dict from Google Sheets with form responses
    
    Returns:
        Mentor object ready for database insertion
    """
    
    mentor = Mentor()
    mentor.name = row.get(COLUMN_MAP["name"], "").strip()
    mentor.email = row.get(COLUMN_MAP["email"], "").strip().lower()
    mentor.form_id = row.get('Timestamp', str(uuid.uuid4()))
    
    # Year in program (dropdown returns full text, map to int)
    mentor.year_in_program = YEAR_MAPPING.get(
        row[COLUMN_MAP["academic_year"]],
        0
    )
    
    # Program
    mentor.program = row.get(COLUMN_MAP["program"], "").strip()
    
    # Specialties (checkboxes come as comma-separated string from Google Forms)
    mentor.specialties = parse_checkbox_field(
        row.get(COLUMN_MAP["specialties"], ''), 
        normalize=True
    )
    
    # Languages (checkboxes)
    mentor.languages = parse_checkbox_field(
        row.get(COLUMN_MAP["languages"], 'English')
    )
    
    # Extracurriculars (checkboxes)
    mentor.extracurricular_interests = parse_checkbox_field(
        row.get(COLUMN_MAP["extracurriculars"], ''),
        normalize=True
    )
    
    # Identity factors (checkboxes)
    mentor.race_ethnicity = parse_checkbox_field(
        row.get(COLUMN_MAP["ethnicity"], ''),
        normalize=True
    )
    
    # LGBTQ+ status (multiple choice)
    lgbtq_raw = row.get(COLUMN_MAP["lgbtq"], 'Prefer not to answer')
    mentor.lgbtq_status = normalize_option(lgbtq_raw)
    
    # Max mentees (multiple choice to int)
    max_mentees_raw = str(row.get(COLUMN_MAP["nb_mentees"], "1")).strip()
    if max_mentees_raw.lower() == "no preference":
        mentor.max_mentees = 4  # using 4 as no preference
    else:
        mentor.max_mentees = int(max_mentees_raw)
    
    # Preferred mentees (long answer - parse names)
    preferred_raw = row.get(COLUMN_MAP["specific_mentees"], '')
    mentor.preferred_mentees = [
        " ".join(name.strip().lower().split())
        for name in preferred_raw.split(',')
        if name.strip()
    ]

    return mentor


def process_mentee_form_submission(row: dict) -> Mentee:
    """
    Convert Google Form row into Mentee database object.
    
    Args:
        row: Dict from Google Sheets with form responses
    
    Returns:
        Mentee object ready for database insertion
    """
    
    mentee = Mentee()
    mentee.name = row.get(COLUMN_MAP["name"], "").strip()
    mentee.email = row.get(COLUMN_MAP["email"], "").strip().lower()
    mentee.form_id = row.get('Timestamp', str(uuid.uuid4()))
    
    # Year in program (dropdown returns full text, map to int)
    mentee.year_in_program = YEAR_MAPPING.get(
        row[COLUMN_MAP["academic_year"]],
        0
    )
    
    # Program
    mentee.program = row.get(COLUMN_MAP["program"], "").strip()
    
    # Specialties (checkboxes come as comma-separated string from Google Forms)
    mentee.specialties = parse_checkbox_field(
        row.get(COLUMN_MAP["specialties"], ''), 
        normalize=True
    )
    
    # Languages (checkboxes)
    mentee.languages = parse_checkbox_field(
        row.get(COLUMN_MAP["languages"], 'English')
    )
    
    # Extracurriculars (checkboxes)
    mentee.extracurricular_interests = parse_checkbox_field(
        row.get(COLUMN_MAP["extracurriculars"], ''),
        normalize=True
    )
    
    # Identity factors (checkboxes)
    mentee.race_ethnicity = parse_checkbox_field(
        row.get(COLUMN_MAP["ethnicity"], ''),
        normalize=True
    )
    
    # LGBTQ+ status (multiple choice)
    lgbtq_raw = row.get(COLUMN_MAP["lgbtq"], 'Prefer not to answer')
    mentee.lgbtq_status = normalize_option(lgbtq_raw)
    
    
    # Preferred mentor (long answer - parse names)
    preferred = row.get(COLUMN_MAP["specific_mentor"], '').strip()

    mentee.preferred_mentor = (
        " ".join(preferred.lower().split())
        if preferred else None
    )
    
    return mentee
