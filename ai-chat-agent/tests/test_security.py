import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent import validate_user_input


def test_accept_valid_input():
    assert validate_user_input("Hello") is True


def test_reject_empty_input():
    assert validate_user_input("") is False


def test_reject_whitespace():
    assert validate_user_input("     ") is False


def test_reject_oversized_input():
    assert validate_user_input("A" * 5001) is False


def test_reject_non_string_input():
    assert validate_user_input(12345) is False


def test_accept_maximum_length():
    assert validate_user_input("A" * 5000) is True