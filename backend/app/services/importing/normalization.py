YEAR_MAPPING = {
    "U0 (Undergraduate Year 0)": 0,
    "U1 (Undergraduate Year 1)": 1,
    "U2 (Undergraduate Year 2)": 2,
    "U3 (Undergraduate Year 3)": 3,
    "M1 (Masters Year 1)": 4,
    "M2 (Masters Year 2)": 5,
    "Graduated": 6
}


def to_str(value):
    return str(value).strip() if value is not None else ""


def to_lower_str(value):
    return to_str(value).lower()


def to_option_str(value):
    return (
        to_str(value)
        .lower()
        .replace(" / ", "/")
        .replace(" ", "_")
    )


def to_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def to_year_int(value):
    s = to_str(value)
    if s in YEAR_MAPPING:
        return YEAR_MAPPING[s]
    return to_int(s, default=0)


def to_max_mentees(value):
    s = to_str(value)
    if s.lower() == "no preference":
        return 4
    return to_int(s, default=1)


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
