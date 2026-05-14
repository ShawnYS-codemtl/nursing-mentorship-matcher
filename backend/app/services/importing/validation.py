def validate_rows(rows, required_fields):

    errors = []

    for index, row in enumerate(rows):

        missing = []

        for field in required_fields:
            if not row.get(field):
                missing.append(field)

        if missing:
            errors.append({
                "row": index + 1,
                "missing": missing
            })

    return errors

REQUIRED_MENTOR_FIELDS = {
    "name",
    "email",
    "program",
    "year_in_program",
    "languages",
    "max_mentees"
}

REQUIRED_MENTEE_FIELDS = {
    "name",
    "email",
    "program",
    "year_in_program",
    "languages_needed"
}