import pytest

from simple_yaml import parse


def test_flat_mapping():
    assert parse("name: tdd\nargument-hint: \"\"") == {"name": "tdd", "argument-hint": ""}


def test_value_may_contain_colon():
    assert parse("description: Dùng khi: viết test") == {"description": "Dùng khi: viết test"}


def test_quoted_values_are_unquoted():
    assert parse("a: \"x: y\"\nb: '#8FA284'") == {"a": "x: y", "b": "#8FA284"}


def test_nested_mapping():
    text = "color:\n  primary: '#8FA284'\n  surface:\n    card: '#FAF7F0'\nradius: 8px"
    assert parse(text) == {
        "color": {"primary": "#8FA284", "surface": {"card": "#FAF7F0"}},
        "radius": "8px",
    }


def test_comments_and_blank_lines_ignored():
    assert parse("# chú thích\n\na: 1  # cuối dòng\n") == {"a": "1"}


def test_hash_inside_quotes_kept():
    assert parse("a: '#fff'") == {"a": "#fff"}


def test_bad_indentation_raises():
    with pytest.raises(ValueError, match="dòng 2"):
        parse("a: 1\n   b: 2")
