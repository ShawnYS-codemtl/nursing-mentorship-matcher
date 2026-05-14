from app.models import Mentor, Mentee
import uuid

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

def build_mentor_from_row(row: dict) -> Mentor:

    mentor = Mentor()

    mentor.name = row.get("name", "").strip()

    mentor.email = (
        row.get("email", "")
        .strip()
        .lower()
    )

    mentor.form_id = str(uuid.uuid4())

    # =========================
    # Year
    # =========================

    raw_year = row.get(
        "year_in_program",
        ""
    ).strip()

    mentor.year_in_program = (
        YEAR_MAPPING.get(raw_year, 0)
    )

    # =========================
    # Program
    # =========================

    mentor.program = (
        row.get("program", "")
        .strip()
    )

    # =========================
    # Specialties
    # =========================

    mentor.specialties = (
        parse_checkbox_field(
            row.get("specialties", ""),
            normalize=True
        )
    )

    # =========================
    # Languages
    # =========================

    mentor.languages = (
        parse_checkbox_field(
            row.get("languages", "English")
        )
    )

    # =========================
    # Extracurriculars
    # =========================

    mentor.extracurricular_interests = (
        parse_checkbox_field(
            row.get(
                "extracurricular_interests",
                ""
            ),
            normalize=True
        )
    )

    # =========================
    # Identity
    # =========================

    mentor.race_ethnicity = (
        parse_checkbox_field(
            row.get(
                "race_ethnicity",
                ""
            ),
            normalize=True
        )
    )

    # =========================
    # LGBTQ
    # =========================

    lgbtq_raw = row.get(
        "lgbtq_status",
        "Prefer not to answer"
    )

    mentor.lgbtq_status = (
        normalize_option(lgbtq_raw)
    )

    # =========================
    # Capacity
    # =========================

    max_mentees_raw = str(
        row.get("max_mentees", "1")
    ).strip()

    if (
        max_mentees_raw.lower()
        == "no preference"
    ):
        mentor.max_mentees = 4
    else:
        mentor.max_mentees = int(max_mentees_raw)

    # =========================
    # Preferred mentees
    # =========================

    preferred_raw = row.get(
        "preferred_mentees_names",
        ""
    )

    mentor.preferred_mentees_names = [
        "_".join(
            name.strip().lower().split()
        )
        for name in preferred_raw.split(",")
        if name.strip()
    ]

    return mentor

def build_mentee_from_row(row: dict) -> Mentee:

    mentee = Mentee()

    mentee.name = row.get("name", "").strip()

    mentee.email = (
        row.get("email", "")
        .strip()
        .lower()
    )

    mentee.form_id = str(uuid.uuid4())

    # =========================
    # Year
    # =========================

    raw_year = row.get(
        "year_in_program",
        ""
    ).strip()

    mentee.year_in_program = (
        YEAR_MAPPING.get(raw_year, 0)
    )

    # =========================
    # Program
    # =========================

    mentee.program = (
        row.get("program", "")
        .strip()
    )

    # =========================
    # Specialties
    # =========================

    mentee.specialties = (
        parse_checkbox_field(
            row.get("specialties", ""),
            normalize=True
        )
    )

    # =========================
    # Languages
    # =========================

    mentee.languages_needed = (
        parse_checkbox_field(
            row.get("languages_needed", "English")
        )
    )

    # =========================
    # Extracurriculars
    # =========================

    mentee.extracurricular_interests = (
        parse_checkbox_field(
            row.get(
                "extracurricular_interests",
                ""
            ),
            normalize=True
        )
    )

    # =========================
    # Identity
    # =========================

    mentee.race_ethnicity = (
        parse_checkbox_field(
            row.get(
                "race_ethnicity",
                ""
            ),
            normalize=True
        )
    )

    # =========================
    # LGBTQ
    # =========================

    lgbtq_raw = row.get(
        "lgbtq_status",
        "Prefer not to answer"
    )

    mentee.lgbtq_status = (
        normalize_option(lgbtq_raw)
    )

    # =========================
    # Preferred mentor
    # =========================

    preferred_raw = row.get("preferred_mentor_name", "")

    mentee.preferred_mentor_name = (
        "_".join(preferred_raw.lower().split())
        if preferred_raw else None
    )

    return mentee