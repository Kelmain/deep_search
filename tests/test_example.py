"""Example test file to verify pytest setup."""

import pytest


def test_basic_functionality():
    """Test basic Python functionality."""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations."""
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert len(text) == 11


def test_list_operations():
    """Test list operations."""
    items = [1, 2, 3, 4, 5]
    assert len(items) == 5
    assert sum(items) == 15
    assert max(items) == 5


@pytest.mark.parametrize(
    "input_val,expected",
    [
        (0, 0),
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
    ],
)
def test_square_function(input_val, expected):
    """Test square function with parametrized values."""
    assert input_val**2 == expected


class TestExampleClass:
    """Example test class."""

    def test_class_method(self):
        """Test method within a class."""
        assert True

    def test_another_method(self):
        """Another test method."""
        data = {"key": "value"}
        assert "key" in data
        assert data["key"] == "value"
