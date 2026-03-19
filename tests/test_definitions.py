"""Tests for definitions.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from definitions import get_yakudoshi_ages, kazoedoshi_to_mannenrei


class TestKazoedoshiConversion:
    def test_default_offset(self):
        assert kazoedoshi_to_mannenrei(42) == 41

    def test_offset_minus2(self):
        assert kazoedoshi_to_mannenrei(42, offset=-2) == 40

    def test_age_1_default(self):
        assert kazoedoshi_to_mannenrei(1) == 0


class TestGetYakudoshiAges:
    def test_male_default(self):
        ages = get_yakudoshi_ages("male")
        assert ages == [24, 41, 60]

    def test_female_default(self):
        ages = get_yakudoshi_ages("female")
        assert ages == [18, 32, 36, 60]

    def test_male_offset_minus2(self):
        ages = get_yakudoshi_ages("male", offset=-2)
        assert ages == [23, 40, 59]

    def test_female_offset_minus2(self):
        ages = get_yakudoshi_ages("female", offset=-2)
        assert ages == [17, 31, 35, 59]

    def test_male_with_mae_ato(self):
        ages = get_yakudoshi_ages("male", include_mae_ato=True)
        # hon-yaku: 24, 41, 60 → ±1 each
        assert 23 in ages and 24 in ages and 25 in ages
        assert 40 in ages and 41 in ages and 42 in ages
        assert 59 in ages and 60 in ages and 61 in ages
        assert len(ages) == 9

    def test_invalid_sex(self):
        import pytest
        with pytest.raises(ValueError, match="sex must be"):
            get_yakudoshi_ages("other")

    def test_sorted(self):
        ages = get_yakudoshi_ages("female", include_mae_ato=True)
        assert ages == sorted(ages)
