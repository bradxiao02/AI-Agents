import sys
from pathlib import Path

import pytest

# Allow Python to import files from the src folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tools import (
    calculator,
    word_counter,
    text_analyzer,
    unit_converter,
    date_and_time
)


# ==========================================
# CALCULATOR TESTS
# ==========================================

def test_calculator_multiplication():
    assert calculator("45 * 9") == 405


def test_calculator_addition():
    assert calculator("20 + 10") == 30


def test_calculator_rejects_division_by_zero():
    try:
        result = calculator("10 / 0")
        assert not isinstance(result, (int, float))
    except (ValueError, ZeroDivisionError):
        pass


# ==========================================
# WORD COUNTER TESTS
# ==========================================

def test_word_counter():
    result = word_counter("I am learning AI agents")

    assert result["words"] == 5
    assert result["characters"] == 23
    assert result["characters_without_spaces"] == 19


# ==========================================
# TEXT ANALYZER TESTS
# ==========================================

def test_text_analyzer():
    text = "AI agents can automate tasks. They use tools."

    result = text_analyzer(text)

    assert result["word_count"] == 8
    assert result["sentence_count"] == 2
    assert result["paragraph_count"] == 1
    assert len(result["most_common_words"]) <= 5


# ==========================================
# UNIT CONVERTER TESTS
# ==========================================

def test_unit_converter():
    result = unit_converter(5, "km", "m")

    assert result["original_value"] == 5
    assert result["from_unit"] == "km"
    assert result["converted_value"] == 5000
    assert result["to_unit"] == "m"


def test_unit_converter_rejects_invalid_units():
    with pytest.raises(ValueError):
        unit_converter(5, "km", "kg")


# ==========================================
# DATE AND TIME TESTS
# ==========================================

def test_date_and_time():
    result = date_and_time()

    assert isinstance(result, str)
    assert len(result) > 0