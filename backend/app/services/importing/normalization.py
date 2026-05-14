def normalize_rows(rows, mapping):

    normalized = []

    for row in rows:

        normalized_row = {}

        for csv_column, canonical_field in mapping.items():

            if canonical_field == "ignore":
                continue

            normalized_row[canonical_field] = row.get(csv_column)

        normalized.append(normalized_row)

    return normalized