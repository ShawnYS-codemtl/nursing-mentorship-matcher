"""Match the names people type into the pairing-request fields against the
names they actually registered with.

Nobody spells someone else's name the way the form recorded it. In the
2026-2027 intake alone, people dropped accents ("Elly Aube" for "Elly Aubé"),
skipped a middle name ("Victoria Bélanger" for "Victoria Kim Belanger"), used a
nickname the other person only put in brackets ("Alex Yam" for "Alexandre
(Alex) Yam"), tacked on a year ("Heidi Pham U2"), lost a space ("Lutong" for
"Lu Tong Wei") and named two people in one answer ("Coralie and Nakia miller").
Exact string matching dropped every one of those, which cost the mutual-match
phase its highest-value pairs.

Matching runs in tiers -- exact, then token-subset, then run-together prefix --
and a tier only counts if exactly one person matches in it. An answer that
fits two people resolves to nobody rather than guessing, and so does free text
like "I don't mind :)".
"""

import re
import unicodedata

# Tacked onto a name to say which year someone is in; never part of the name.
_YEAR_TOKEN = re.compile(r"^(u[0-6]|m[12]|y[1-6]|year|grad|graduated)$")

# People list two names in one answer with these, e.g. "Coralie and Nakia".
_NAME_SEPARATORS = re.compile(r"\s+and\s+|\s*&\s*|\s*/\s*|\s*;\s*|\n", re.IGNORECASE)

# "(Alex)" or "[Fiona Lam]" -- a nickname worth indexing when it is short, and
# an aside worth ignoring when it is long ("(if she'd like to be paired...)").
_BRACKETED = re.compile(r"[\(\[]([^\)\]]*)[\)\]]")

_MAX_NICKNAME_TOKENS = 2
_MIN_PREFIX_LENGTH = 4


def strip_accents(text):
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def _tokens(text):
    """Split a name into comparable word tokens.

    Accents, punctuation, case and year suffixes all disappear, so
    "Phédora-Lee Joseph" and "phedora lee joseph" become the same tokens.
    """
    if not text:
        return set()

    cleaned = strip_accents(str(text)).lower()
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned)

    return {
        token
        for token in cleaned.split()
        if len(token) > 1 and not _YEAR_TOKEN.match(token)
    }


def _candidate_tokens(name):
    """Tokens a registered name can be found by, including a short nickname.

    "Alexandre (Alex) Yam" is findable as alexandre, alex or yam. A long
    bracketed aside is dropped rather than indexed as if it were a name.
    """
    nicknames = set()

    for bracketed in _BRACKETED.findall(name or ""):
        tokens = _tokens(bracketed)
        if 0 < len(tokens) <= _MAX_NICKNAME_TOKENS:
            nicknames |= tokens

    return _tokens(_BRACKETED.sub(" ", name or "")) | nicknames


def _query_tokens(text):
    """Tokens from what someone typed, with any parenthetical aside removed."""
    return _tokens(_BRACKETED.sub(" ", text or ""))


def _joined(tokens):
    return "".join(sorted(tokens))


def build_index(people):
    """Pair each person with the tokens their name can be matched on."""
    return [(person, _candidate_tokens(person.name)) for person in people]


def _match_one(query, index):
    """Resolve a single typed name, or None if it is unclear who is meant."""
    query_tokens = _query_tokens(query)

    if not query_tokens:
        return None

    exact, subset, prefix = [], [], []

    for person, tokens in index:
        if not tokens:
            continue

        if query_tokens == tokens:
            exact.append(person)
            continue

        # "Victoria Belanger" inside "Victoria Kim Belanger", or a bare
        # "Elly" inside "Elly Aube". A one-token registered name is not
        # matched this way, so a sentence cannot swallow it by accident.
        if query_tokens < tokens or (len(tokens) > 1 and tokens < query_tokens):
            subset.append(person)
            continue

        # "Lutong" for "Lu Tong Wei" -- spaces dropped between name parts.
        query_joined, person_joined = _joined(query_tokens), _joined(tokens)
        if len(query_joined) >= _MIN_PREFIX_LENGTH and person_joined.startswith(query_joined):
            prefix.append(person)

    for tier in (exact, subset, prefix):
        if len(tier) == 1:
            return tier[0]
        if tier:
            return None  # ambiguous at this tier; guessing would be worse

    return None


def resolve_names(raw, index):
    """Resolve one form answer into the people it names, in the order typed.

    One answer can name several people ("Coralie and Nakia miller"), so this
    returns a list. Free text that names nobody returns an empty list.
    """
    if not raw:
        return []

    resolved = []

    for part in _NAME_SEPARATORS.split(str(raw)):
        person = _match_one(part, index)

        if person is not None and person not in resolved:
            resolved.append(person)

    return resolved
