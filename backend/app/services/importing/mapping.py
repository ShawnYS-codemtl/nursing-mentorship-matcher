from aliases import MENTEE_ALIASES, MENTOR_ALIASES

def normalize_column_name(name):
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
    )

def detect_mapping(columns, column_aliases):
    mapping = {}
    unmatched = []

    for original_col in columns:
        normalized_col = normalize_column_name(original_col)

        matched_field = None

        # ---- Exact match ----
        for canonical_field, aliases in column_aliases.items():
            normalized_aliases = [
                normalize_column_name(a)
                for a in aliases
            ]

            if normalized_col in normalized_aliases:
                matched_field = canonical_field
                break

        # ---- Containment match ----
        if not matched_field:
            for canonical_field, aliases in column_aliases.items():

                normalized_aliases = [
                    normalize_column_name(a)
                    for a in aliases
                ]

                for alias in normalized_aliases:
                    if alias in normalized_col:
                        matched_field = canonical_field
                        break

                if matched_field:
                    break

        if matched_field:
            mapping[original_col] = matched_field
        else:
            unmatched.append(original_col)

    return mapping, unmatched