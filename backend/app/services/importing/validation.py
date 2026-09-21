from app.services.importing.name_matching import strip_accents

# The program runs in English and French, so a mentor who speaks neither, or a
# mentee who asks for neither, can never satisfy the language constraint in
# scoring and would silently sit unmatched. Spelling varies ("Francais",
# "anglais"), so match on the word appearing anywhere in the answer.
SUPPORTED_LANGUAGE_WORDS = ("english", "anglais", "french", "francais")


def is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""


def is_positive_int(value):
    return isinstance(value, int) and value >= 0


def is_list(value):
    return isinstance(value, list)


def has_supported_language(value):
    """True when at least one answer names English or French."""
    if not is_list(value):
        return False

    return any(
        word in strip_accents(str(entry)).lower()
        for entry in value
        for word in SUPPORTED_LANGUAGE_WORDS
    )


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

    "languages": has_supported_language,

    "languages_needed": has_supported_language,

    "max_mentees": is_positive_int,

    "specialties": is_list,

    "race_ethnicity": is_list,

    "lgbtq_status": is_non_empty_string,

    "extracurricular_interests": is_list
}

# Shown next to a rejected value so the admin knows what to fix, rather than
# just being told the value is invalid.
FIELD_ERROR_REASONS = {
    "languages": "must list English or French",
    "languages_needed": "must list English or French",
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

                invalid_field = {
                    "field": field,
                    "value": value
                }

                reason = FIELD_ERROR_REASONS.get(field)
                if reason:
                    invalid_field["reason"] = reason

                invalid_types.append(invalid_field)

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