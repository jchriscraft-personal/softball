# pylint: disable=C0116
# pylint: disable=C0114
# pylint: disable=W0703
from geography_helper import state_name_to_abbrev


def test_valid_lower_case():
    abbrv = state_name_to_abbrev("wyoming")
    assert abbrv == "WY"


def test_valid_pascal_case():
    abbrv = state_name_to_abbrev("Rhode Island")
    assert abbrv == "RI"


def test_valid_upper_case():
    abbrv = state_name_to_abbrev("TEXAS")
    assert abbrv == "TX"


def test_invalid():
    all_good = False
    try:
        state_name_to_abbrev("abc")
    except Exception as ex:
        if isinstance(ex, KeyError):
            all_good = True
        assert all_good is True
