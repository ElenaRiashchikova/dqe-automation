from pathlib import Path
import pytest
import re
import os
import csv
import pandas as pd
import pathlib

path_to_file = next(Path.cwd().rglob("data.csv"), None)


def test_file_not_empty():
    # Assert file is not empty
    assert os.stat(path_to_file).st_size > 0, f"File '{path_to_file}' is empty!"

def test_data_rows_present():
    # Assert that the file contains only the header (no data rows)
    with open(path_to_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        assert len(rows) > 1, f"File '{path_to_file}' contains no data rows!"

def test_validate_schema():
    EXPECTED_HEADER = ["id", "name", "age", "email", "is_active"]
    df = pd.read_csv(path_to_file)
    actual_header = list(df.columns)
    assert actual_header == EXPECTED_HEADER, (
        f"Header mismatch.\nExpected: {EXPECTED_HEADER}\nFound: {actual_header}"
    )

@pytest.mark.skipif(os.stat(path_to_file).st_size == 0, reason="CSV file is empty")
@pytest.mark.parametrize("age_value", pd.read_csv(path_to_file)["age"].tolist() if os.stat(path_to_file).st_size > 0 else [])
def test_age_column_valid(age_value):
    assert 0 <= int(age_value) <= 100, f"Age '{age_value}' is out of range (1-100)"


EMAIL_COLUMN = "email"
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"

def validate_email(email: str) -> bool:
    """Return True if email matches regex, else False."""
    return bool(re.match(EMAIL_REGEX, email))

def test_email_column_valid():
    with open(path_to_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        assert EMAIL_COLUMN in reader.fieldnames, f"Column '{EMAIL_COLUMN}' not found in CSV header."

        for row in reader:
            email = row[EMAIL_COLUMN].strip()
            assert validate_email(email), f"Invalid email found: {email}"


def test_duplicates():

    with open(path_to_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        # Skip header
        data_rows = rows[1:]
        # Normalize rows: strip spaces and hidden characters
        normalized_rows = [tuple(cell.strip() for cell in row) for row in data_rows]
        seen = set()
        duplicates = []
        for row in normalized_rows:
            if row in seen:
                duplicates.append(row)
            else:
                seen.add(row)
        assert not duplicates, f"Duplicate rows found: {duplicates}"


def _load_is_active(path_to_file: pathlib.Path) -> dict[int, bool]:
    mapping = {}
    with path_to_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid = int(row["id"].strip())
            mapping[rid] = row["is_active"].strip().lower() == "true"
    return mapping

@pytest.mark.parametrize(
    ("id", "expected"),
    [
        (1, False),
        (2, True),
    ],
)

def test_active_players(id, expected):
    rpath_to_file = pathlib.Path(__file__).with_name("data.csv")
    actual = _load_is_active(path_to_file)
    assert actual[id] == expected, f'IS_ACTIVE not valid for ID {id}'


def test_active_player():
    rpath_to_file = pathlib.Path(__file__).with_name("data.csv")
    actual = _load_is_active(path_to_file)
    assert actual[2] is True, f'IS_ACTIVE not valid for ID 2'
