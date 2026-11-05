# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

"""Filter CSV text with a read-only SQL WHERE clause (in-memory SQLite)."""

import csv
import io
import math
import re
import sqlite3

# Forbidden SQL keywords (mutating/DDL statements); only a read-only
# WHERE clause against the in-memory table is allowed.
FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH"
    r"|REPLACE|PRAGMA|REINDEX|VACUUM|SAVEPOINT|RELEASE"
    r"|BEGIN|COMMIT|ROLLBACK)\b",
    re.IGNORECASE,
)


def parse_number(cell_value, thousand_sep=",", decimal_sep="."):
    """Parse a CSV cell into a float, or ``None`` when not numeric.

    Parenthesised values are negative, ``(100)`` -> ``-100``.

    :param cell_value: raw cell text from the CSV.
    :param thousand_sep: thousand separator used in ``cell_value``.
    :param decimal_sep: decimal separator used in ``cell_value``.
    :return: the parsed float, or ``None`` for a non-numeric cell.
    """
    raw_val = (cell_value or "").strip()
    if raw_val.startswith("(") and raw_val.endswith(")"):
        raw_val = "-" + raw_val[1:-1]
    if thousand_sep:
        raw_val = raw_val.replace(thousand_sep, "")
    if decimal_sep and decimal_sep != ".":
        raw_val = raw_val.replace(decimal_sep, ".")
    try:
        number = float(raw_val)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def sanitize_columns(headers):
    """Turn CSV header labels into usable SQLite column names.

    Characters outside ``\\w`` become ``_``, a leading digit gets a
    ``c_`` prefix, and names that collide (case-insensitively, or with
    a SQLite row-id alias) get a numeric suffix.

    :param headers: the CSV header labels.
    :return: a list of unique column names, one per header.
    """
    reserved = {"rowid", "oid", "_rowid_"}
    used = set()
    result = []
    for label in headers:
        col = re.sub(r"[^\w]", "_", label.strip())
        if not col or col[0].isdigit():
            col = "c_" + col
        candidate = col
        counter = 2
        while candidate.lower() in used or candidate.lower() in reserved:
            candidate = "{}_{}".format(col, counter)
            counter += 1
        used.add(candidate.lower())
        result.append(candidate)
    return result


def describe_columns(raw_csv):
    """List the column names a WHERE clause may reference.

    :param raw_csv: CSV text with a header row.
    :return: the sanitised column names joined by commas, or an empty
        string when ``raw_csv`` has no header.
    """
    headers = next(csv.reader(io.StringIO(raw_csv or "")), None)
    return ", ".join(sanitize_columns(headers)) if headers else ""


def filter_csv(raw_csv, where_clause, thousand_sep=",", decimal_sep="."):
    """Filter CSV data with a read-only SQL WHERE clause via SQLite.

    A column whose non-blank cells all parse as numbers (using the
    given separators) gets NUMERIC affinity and holds the parsed
    values, so ``Debit > 1000`` compares by value even when the cells
    read ``1,500.00`` or ``(2,000.00)``. Other columns stay TEXT. The
    returned rows keep the original cell text.

    :param raw_csv: CSV text with a header row.
    :param where_clause: a SQL WHERE clause (without the ``WHERE``
        keyword) referencing the sanitised column names.
    :param thousand_sep: thousand separator used in the data.
    :param decimal_sep: decimal separator used in the data.
    :return: the filtered CSV text, or ``raw_csv`` unchanged when it or
        ``where_clause`` is empty.
    :raises ValueError: when ``where_clause`` has a forbidden keyword.
    :raises sqlite3.Error: when SQLite cannot run the clause.
    """
    where_clause = (where_clause or "").strip()
    if not where_clause or not raw_csv:
        return raw_csv
    if FORBIDDEN_SQL.search(where_clause):
        raise ValueError("Forbidden SQL keyword in the filter.")

    reader = csv.reader(io.StringIO(raw_csv))
    headers = next(reader, None)
    rows = list(reader)
    if not headers or not rows:
        return raw_csv

    safe_cols = sanitize_columns(headers)
    width = len(safe_cols)
    padded_rows = [(list(row) + [""] * width)[:width] for row in rows]

    parsed_cols = []
    col_types = []
    for i in range(width):
        values = [
            parse_number(row[i], thousand_sep, decimal_sep) for row in padded_rows
        ]
        numeric_col = all(
            value is not None or not row[i].strip()
            for value, row in zip(values, padded_rows)
        ) and any(value is not None for value in values)
        col_types.append("NUMERIC" if numeric_col else "TEXT")
        parsed_cols.append(values)

    col_defs = ", ".join('"{}" {}'.format(c, t) for c, t in zip(safe_cols, col_types))
    placeholders = ", ".join(["?"] * width)

    conn = sqlite3.connect(":memory:")
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE data ({})".format(col_defs))
        for idx, row in enumerate(padded_rows):
            cells = [
                parsed_cols[i][idx] if col_types[i] == "NUMERIC" else row[i]
                for i in range(width)
            ]
            cur.execute("INSERT INTO data VALUES ({})".format(placeholders), cells)
        cur.execute(
            "SELECT rowid FROM data WHERE {} ORDER BY rowid".format(where_clause)
        )
        kept = [rowid - 1 for (rowid,) in cur.fetchall()]
    finally:
        conn.close()

    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(headers)
    writer.writerows(padded_rows[idx] for idx in kept)
    return out.getvalue()
