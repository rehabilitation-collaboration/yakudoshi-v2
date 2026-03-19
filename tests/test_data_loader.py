"""Tests for data_loader.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_loader import load_analysis_data, load_deaths, load_exposures, load_rates


class TestLoadDeaths:
    def test_loads_dataframe(self):
        df = load_deaths()
        assert len(df) > 0
        assert set(df.columns) == {"year", "age", "female", "male", "total"}

    def test_year_range(self):
        df = load_deaths()
        assert df["year"].min() == 1947
        assert df["year"].max() == 2024

    def test_age_range(self):
        df = load_deaths()
        assert df["age"].min() == 0
        assert df["age"].max() == 110

    def test_no_negative_values(self):
        df = load_deaths()
        assert (df["female"] >= 0).all()
        assert (df["male"] >= 0).all()


class TestLoadExposures:
    def test_loads_dataframe(self):
        df = load_exposures()
        assert len(df) > 0

    def test_positive_exposure(self):
        df = load_exposures()
        # Allow zero for very old ages with no population
        assert (df["female"] >= 0).all()
        assert (df["male"] >= 0).all()


class TestLoadRates:
    def test_loads_dataframe(self):
        df = load_rates()
        assert len(df) > 0

    def test_rates_non_negative(self):
        df = load_rates()
        # NaN allowed for missing data at extreme ages
        assert (df["female"].dropna() >= 0).all()
        assert (df["male"].dropna() >= 0).all()


class TestLoadAnalysisData:
    def test_long_format(self):
        df = load_analysis_data()
        assert "sex" in df.columns
        assert set(df["sex"].unique()) == {"male", "female"}

    def test_columns(self):
        df = load_analysis_data()
        expected = {"year", "age", "sex", "deaths", "exposure", "rate"}
        assert set(df.columns) == expected

    def test_rate_computation(self):
        df = load_analysis_data()
        # rate should equal deaths / exposure (where exposure > 0)
        valid = df["exposure"] > 0
        computed = df.loc[valid, "deaths"] / df.loc[valid, "exposure"]
        diff = (df.loc[valid, "rate"] - computed).abs()
        assert (diff < 1e-10).all()

    def test_row_count(self):
        deaths = load_deaths()
        df = load_analysis_data()
        # long format: 2x the number of rows in deaths (male + female)
        assert len(df) == 2 * len(deaths)
