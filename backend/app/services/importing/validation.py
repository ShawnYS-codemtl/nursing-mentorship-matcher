def is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""


def is_positive_int(value):
    return isinstance(value, int) and value >= 0


def is_list(value):
    return isinstance(value, list)


def is_email(value):
    return (
        isinstance(value, str)
        and "@" in value
        and "." in value
    )

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

FIELD_VALIDATORS = {

    "name": is_non_empty_string,

    "email": is_email,

    "program": is_non_empty_string,

    "year_in_program": is_positive_int,

    "languages": is_list,

    "languages_needed": is_list,

    "max_mentees": is_positive_int,

    "specialties": is_list,

    "race_ethnicity": is_list,

    "lgbtq_status": is_non_empty_string,

    "extracurricular_interests": is_list
}

# def validate_rows(rows, required_fields):

#     errors = []

#     for index, row in enumerate(rows):

#         missing = []

#         for field in required_fields:
#             if not row.get(field):
#                 missing.append(field)

#         if missing:
#             errors.append({
#                 "row": index + 1,
#                 "missing": missing
#             })

#     return errors

def validate_rows(rows, required_fields):

    errors = []

    for index, row in enumerate(rows):

        row_errors = {}

        # =========================
        # Required fields
        # =========================

        missing = []

        for field in required_fields:

            value = row.get(field)

            if value is None or value == "":
                missing.append(field)

        if missing:
            row_errors["missing_fields"] = missing

        # =========================
        # Type validation
        # =========================

        invalid_types = []

        for field, validator in FIELD_VALIDATORS.items():

            if field not in row:
                continue

            value = row[field]

            if not validator(value):

                invalid_types.append({
                    "field": field,
                    "value": value
                })

        if invalid_types:
            row_errors["invalid_fields"] = invalid_types

        # =========================
        # Save row errors
        # =========================

        if row_errors:

            errors.append({
                "row": index + 1,
                **row_errors
            })

    return errors