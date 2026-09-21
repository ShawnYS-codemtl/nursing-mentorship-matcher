# Column-header vocabulary for detect_mapping().
#
# Order matters: detect_mapping() claims each canonical field for the first
# column that matches it, and tries fields in the order listed here. "name" and
# "email" come first because the McGill forms put those words inside unrelated
# questions ("*preferred name in brackets*", "include your name, email"), and
# the genuine name/email columns always appear earlier in the sheet.
#
# Aliases are matched by containment against the lowercased, underscored header,
# so keep them specific enough not to swallow a neighbouring question.

MENTOR_ALIASES = {
    "name": [
        "full_name",
        "name"
    ],

    "email": [
        "email",
        "email_address"
    ],

    "program": [
        "program",
        "program_of_study",
        "degree"
    ],

    "year_in_program": [
        "year_will_you_be_in",
        "year_in_the_program",
        "academic_year",
        "current_year"
    ],

    "max_mentees": [
        "comfortable",
        "how many",
        "max_mentees",
        "maximum_mentees",
        "number_of_mentees",
        "capacity"
    ],

    "preferred_mentees_names": [
        "paired_with_them",
        "paired",
        "specific",
        "preferred"
    ],

    "languages": [
        "language_preference",
        "languages",
        "language"
    ],

    "specialties": [
        "nursing_interests",
        "areas_of_nursing",
        "specialties",
        "specialty",
        "clinical_interests"
    ],

    "race_ethnicity": [
        "shared_experiences",
        "ethnicity",
        "identify"
    ],

    "extracurricular_interests": [
        "extracurricular"
    ],

    "lgbtq_status": [
        "lgbtq_status",
        "2slgbtqi+_status"
    ]
}

MENTEE_ALIASES = {
    "name": [
        "full_name",
        "name"
    ],

    "email": [
        "email",
        "email_address"
    ],

    "program": [
        "program",
        "program_of_study",
        "degree"
    ],

    "year_in_program": [
        "year_will_you_be_in",
        "year_in_the_program",
        "academic_year",
        "current_year"
    ],

    "preferred_mentor_name": [
        "paired_with",
        "paired",
        "specific",
        "preferred"
    ],

    # Mentees store this as languages_needed; naming the key "languages" mapped
    # every mentee CSV onto a field the mentee schema does not have, so the
    # auto-detected mapping always failed validation.
    "languages_needed": [
        "language_preference",
        "languages",
        "language"
    ],

    "specialties": [
        "nursing_interests",
        "areas_of_nursing",
        "specialties",
        "specialty",
        "clinical_interests"
    ],

    "race_ethnicity": [
        "shared_experiences",
        "ethnicity",
        "identify"
    ],

    "extracurricular_interests": [
        "extracurricular"
    ],

    "lgbtq_status": [
        "lgbtq_status",
        "2slgbtqi+_status"
    ]
}
