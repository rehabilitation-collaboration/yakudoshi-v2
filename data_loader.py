"""Load and parse JMD (Japanese Mortality Database) data files."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def _parse_jmd_file(filename: str) -> pd.DataFrame:
    """Parse a JMD 1x1 format file into a DataFrame.

    JMD files have:
    - Line 1: header comment
    - Line 2: blank
    - Line 3: column headers (Year, Age, Female, Male, Total)
    - Lines 4+: data (whitespace-separated)
    - Age "110+" is the open-ended interval
    """
    filepath = DATA_DIR / filename
    rows = []
    with open(filepath) as f:
        lines = f.readlines()

    for line in lines[3:]:  # skip header, blank, column names
        parts = line.split()
        if len(parts) != 5:
            continue
        year = int(parts[0])
        age_str = parts[1]
        age = 110 if age_str == "110+" else int(age_str)
        female = float(parts[2]) if parts[2] != "." else float("nan")
        male = float(parts[3]) if parts[3] != "." else float("nan")
        total = float(parts[4]) if parts[4] != "." else float("nan")
        rows.append({
            "year": year,
            "age": age,
            "female": female,
            "male": male,
            "total": total,
        })

    return pd.DataFrame(rows)


def load_deaths() -> pd.DataFrame:
    """Load Deaths_1x1.txt."""
    return _parse_jmd_file("Deaths_1x1.txt")


def load_exposures() -> pd.DataFrame:
    """Load Exposures_1x1.txt."""
    return _parse_jmd_file("Exposures_1x1.txt")


def load_rates() -> pd.DataFrame:
    """Load Mx_1x1.txt (death rates)."""
    return _parse_jmd_file("Mx_1x1.txt")


def load_analysis_data() -> pd.DataFrame:
    """Load deaths and exposures, compute rates, return merged DataFrame.

    Returns:
        DataFrame with columns: year, age, sex, deaths, exposure, rate
        (long format, one row per year × age × sex)
    """
    deaths = load_deaths()
    exposures = load_exposures()

    records = []
    for sex in ("male", "female"):
        df = pd.DataFrame({
            "year": deaths["year"],
            "age": deaths["age"],
            "sex": sex,
            "deaths": deaths[sex],
            "exposure": exposures[sex],
        })
        df["rate"] = df["deaths"] / df["exposure"]
        records.append(df)

    result = pd.concat(records, ignore_index=True)
    return result
