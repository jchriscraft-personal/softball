# pylint: disable=C0116
# pylint: disable=C0114
from text_helper import parse_name


def test_two_names():
    first_name, last_name = parse_name("Bob Smith")
    assert first_name == "Bob"
    assert last_name == "Smith"


def test_one_name():
    first_name, last_name = parse_name("Bob")
    assert first_name == "Bob"
    assert last_name is None


def test_three_name():
    first_name, last_name = parse_name("Bob Apple Smith")
    assert first_name == "Bob"
    assert last_name == "Apple Smith"


def test_empty_first_name():
    first_name, last_name = parse_name(" Smith")
    assert first_name == ""
    assert last_name == "Smith"


def test_empty_name():
    first_name, last_name = parse_name("")
    assert first_name is None
    assert last_name is None


def test_none_name():
    first_name, last_name = parse_name(None)
    assert first_name is None
    assert last_name is None
