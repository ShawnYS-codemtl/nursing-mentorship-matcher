def normalize_column_name(name):
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
    )

def detect_mapping(columns, column_aliases):
    """Map each CSV column onto at most one canonical field.

    A canonical field is claimed by the first column that matches it. Later
    columns that would match the same field are left unmatched instead of
    silently double-mapping it -- Google Forms templates repeat words like
    "name", "email" and "academic year" in unrelated questions ("include your
    name, email", "would you like to be added to our mailing list"), and the
    real question is almost always the earlier column.
    """
    mapping = {}
    unmatched = []
    claimed = set()

    for original_col in columns:
        normalized_col = normalize_column_name(original_col)

        matched_field = None

        # ---- Exact match ----
        for canonical_field, aliases in column_aliases.items():
            if canonical_field in claimed:
                continue

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
                if canonical_field in claimed:
                    continue

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
            claimed.add(matched_field)
        else:
            unmatched.append(original_col)

    return mapping, unmatched