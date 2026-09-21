# test_name_matching_manual.py
"""Quick manual tests for resolving typed names onto registered people.

Every case here is taken from the 2026-2027 intake, where exact matching
resolved only 2 of the 16 pairing requests people actually made.
"""

from app.services.importing.name_matching import build_index, resolve_names


class Person:
    """Stand-in for a Mentor/Mentee row; the matcher only reads id and name."""

    def __init__(self, id, name):
        self.id = id
        self.name = name


PEOPLE = [
    Person(1, "Victoria Kim Belanger"),
    Person(2, "Heidi, Pham"),
    Person(3, "Elly Aubé"),
    Person(4, "Alexandre (Alex) Yam"),
    Person(5, "Lu Tong Wei"),
    Person(6, "Coralie Remarais"),
    Person(7, "Nakia Miller"),
    Person(8, "Sam Robitaille"),
    Person(9, "Raluca-Mara Mare [ or Mara for short ]"),
    Person(10, "Nguyen"),
]

INDEX = build_index(PEOPLE)


def resolve(text):
    return [p.name for p in resolve_names(text, INDEX)]


def check(label, text, expected):
    actual = resolve(text)
    assert actual == expected, f"{label}: {text!r} -> {actual}, expected {expected}"
    print(f"✓ {label}")
    print(f"  {text!r} -> {actual}")


def test_exact_name():
    check("Exact name", "Sam Robitaille", ["Sam Robitaille"])


def test_missing_accent():
    check("Missing accent", "Elly Aube", ["Elly Aubé"])


def test_skipped_middle_name():
    check("Skipped middle name", "Victoria Bélanger", ["Victoria Kim Belanger"])


def test_first_name_only():
    check("First name only", "Elly", ["Elly Aubé"])


def test_bracketed_nickname():
    check("Bracketed nickname", "Alex Yam", ["Alexandre (Alex) Yam"])


def test_year_suffix():
    check("Year suffix", "Heidi Pham U2", ["Heidi, Pham"])


def test_missing_space():
    check("Missing space", "Lutong", ["Lu Tong Wei"])


def test_two_people_in_one_answer():
    check(
        "Two people in one answer",
        "Coralie and Nakia miller",
        ["Coralie Remarais", "Nakia Miller"],
    )


def test_free_text_matches_nobody():
    check("Free text", "I don't mind :)", [])
    check("Free text with a stranger", "Yes and Liz Jolicoeur", [])
    check("Non-answer", "No preference", [])


def test_unregistered_person():
    check("Unregistered person", "Davyne Alexa Bolduc", [])


def test_long_aside_is_ignored():
    # The aside must not be indexed as a name, and must not stop the real
    # name in front of it from being read.
    check(
        "Long parenthetical aside",
        "Sam Robitaille (if he'd like to be paired with me again)",
        ["Sam Robitaille"],
    )
    check("Aside text alone", "or Mara for short", [])


def test_short_name_not_swallowed_by_a_sentence():
    # "Nguyen" is a single token; a sentence that happens to contain it
    # should not silently resolve to that person.
    check("Single-token name in prose", "nguyen", ["Nguyen"])
    check("Sentence containing the token", "ask nguyen or whoever is free", [])


def test_ambiguous_answer_resolves_to_nobody():
    people = [Person(1, "Sarah Chen"), Person(2, "Sarah Diaz")]
    index = build_index(people)
    actual = [p.name for p in resolve_names("Sarah", index)]
    assert actual == [], f"Ambiguous 'Sarah' -> {actual}, expected []"
    print("✓ Ambiguous first name")
    print("  'Sarah' with two Sarahs -> []")


def test_everyone_resolves_to_themselves():
    for person in PEOPLE:
        actual = resolve_names(person.name, INDEX)
        assert len(actual) == 1 and actual[0].id == person.id, (
            f"{person.name!r} did not resolve to itself: {[p.name for p in actual]}"
        )
    print("✓ Every registered name resolves to itself")
    print(f"  checked {len(PEOPLE)} names")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTING resolve_names FUNCTION")
    print("=" * 60)

    test_exact_name()
    test_missing_accent()
    test_skipped_middle_name()
    test_first_name_only()
    test_bracketed_nickname()
    test_year_suffix()
    test_missing_space()
    test_two_people_in_one_answer()
    test_free_text_matches_nobody()
    test_unregistered_person()
    test_long_aside_is_ignored()
    test_short_name_not_swallowed_by_a_sentence()
    test_ambiguous_answer_resolves_to_nobody()
    test_everyone_resolves_to_themselves()

    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60 + "\n")
