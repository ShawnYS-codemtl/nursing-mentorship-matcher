import re

# Labels from the 2026-2027 forms, plus the older long-form labels so that
# CSVs exported from previous years still import. Values are an ordering, not a
# count of years: matching only requires mentor.year > mentee.year.
YEAR_MAPPING = {
    "U0": 0,
    "U1": 1,
    "U2": 2,
    "U3": 3,
    "Master's Year 1": 4,
    "Master's Year 2": 5,
    "Graduated": 6,

    # Retired 2025-2026 wording
    "U0 (Undergraduate Year 0)": 0,
    "U1 (Undergraduate Year 1)": 1,
    "U2 (Undergraduate Year 2)": 2,
    "U3 (Undergraduate Year 3)": 3,
    "M1 (Masters Year 1)": 4,
    "M2 (Masters Year 2)": 5,
}

# Unrecognized option strings are returned as-is rather than defaulted, so that
# validate_rows() reports them and the admin sees the offending value on the
# import screen. Defaulting silently (year 0) makes every match fail the year
# constraint with nothing to explain why.
NO_PREFERENCE = "no preference"


def to_str(value):
    return str(value).strip() if value is not None else ""


def canonical_option(value):
    """Fold the cosmetic differences Google Forms introduces between template
    revisions: casing, doubled spaces, and curly quotes substituted for straight
    ones (e.g. Master's). Genuine rewording still misses, which is intended."""
    return re.sub(
        r"\s+", " ",
        to_str(value).lower().replace("’", "'").replace("‘", "'")
    ).strip()


_YEAR_LOOKUP = {canonical_option(k): v for k, v in YEAR_MAPPING.items()}


def to_lower_str(value):
    return to_str(value).lower()


def to_option_str(value):
    return (
        to_str(value)
        .lower()
        .replace(" / ", "/")
        .replace(" ", "_")
    )


def to_year_int(value):
    s = to_str(value)
    year = _YEAR_LOOKUP.get(canonical_option(s))
    if year is not None:
        return year
    if s.isdigit():
        return int(s)
    return s  # unrecognized: surfaced by validate_rows() instead of becoming 0


def to_max_mentees(value):
    s = to_str(value)
    if canonical_option(s) == NO_PREFERENCE:
        return 4
    if s.isdigit():
        return int(s)
    return s  # unrecognized: surfaced by validate_rows() instead of becoming 1


def to_list(value):
    if not value:
        return []
    return [v.strip() for v in str(value).split(",") if v.strip()]


def to_normalized_list(value):
    return [
        v.lower().replace(" ", "_")
        for v in to_list(value)
    ]


FIELD_CONVERTERS = {
    "name":                      to_str,
    "email":                     to_lower_str,
    "program":                   to_str,
    "year_in_program":           to_year_int,
    "languages":                 to_list,
    "languages_needed":          to_list,
    "max_mentees":               to_max_mentees,
    "specialties":               to_normalized_list,
    "race_ethnicity":            to_normalized_list,
    "lgbtq_status":              to_option_str,
    "extracurricular_interests": to_normalized_list,
    "preferred_mentees_names":   to_list,
    "preferred_mentor_name":     to_str,
}


def normalize_rows(rows, mapping):
    normalized = []
    for row in rows:
        normalized_row = {}
        for csv_column, canonical_field in mapping.items():
            if canonical_field == "ignore":
                continue
            raw = row.get(csv_column)
            converter = FIELD_CONVERTERS.get(canonical_field)
            normalized_row[canonical_field] = converter(raw) if converter else raw
        normalized.append(normalized_row)
    return normalized
