# test_validation_manual.py
"""Quick manual tests for row validation.

The language check exists because a mentor who speaks neither English nor
French can never satisfy the language constraint in scoring: they import
cleanly, then sit unmatched with no explanation. One mentor in the 2026-2027
intake answered the language question with "Both", which is what prompted it.
"""

from app.services.importing.validation import (
    has_supported_language,
    validate_rows,
    REQUIRED_MENTOR_FIELDS,
)


def check(label, value, expected):
    actual = has_supported_language(value)
    assert actual == expected, f"{label}: {value!r} -> {actual}, expected {expected}"
    print(f"✓ {label}")
    print(f"  {value!r} -> {'accepted' if actual else 'rejected'}")


def test_english_or_french_accepted():
    check("English", ["English"], True)
    check("French", ["French"], True)
    check("Lowercase", ["english"], True)
    check("Accented French", ["Français"], True)
    check("French spelled without the accent", ["Francais"], True)
    check("Other languages alongside English", ["English", "Chinese mandarin"], True)
    check("Free text alongside English", ["English", "I am happy with both!"], True)


def test_neither_language_rejected():
    check("Neither language", ["Spanish"], False)
    check("Ambiguous answer", ["Both"], False)
    check("No answer", [], False)


def test_non_list_rejected():
    check("Bare string", "English", False)
    check("None", None, False)


def test_error_explains_itself():
    rows = [{
        "name": "Melissa Natashah",
        "email": "melissa@mail.mcgill.ca",
        "program": "BScN",
        "year_in_program": 3,
        "languages": ["Both"],
        "max_mentees": 4,
    }]

    errors = validate_rows(rows, REQUIRED_MENTOR_FIELDS)

    assert len(errors) == 1, f"expected 1 rejected row, got {errors}"

    invalid = errors[0]["invalid_fields"]
    assert len(invalid) == 1 and invalid[0]["field"] == "languages", invalid
    assert invalid[0]["reason"] == "must list English or French", invalid

    print("✓ Rejected row explains why")
    print(f"  {errors[0]}")


def test_valid_row_passes():
    rows = [{
        "name": "Hong Wei Liu",
        "email": "hong@mail.mcgill.ca",
        "program": "BScN",
        "year_in_program": 3,
        "languages": ["English", "French", "Chinese mandarin"],
        "max_mentees": 2,
    }]

    errors = validate_rows(rows, REQUIRED_MENTOR_FIELDS)

    assert errors == [], f"expected no errors, got {errors}"
    print("✓ Valid row passes")
    print("  no errors")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTING row validation")
    print("=" * 60)

    test_english_or_french_accepted()
    test_neither_language_rejected()
    test_non_list_rejected()
    test_error_explains_itself()
    test_valid_row_passes()

    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60 + "\n")
