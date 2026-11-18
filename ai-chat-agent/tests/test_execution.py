import sys
from pathlib import Path

# Allow Python to import files from src.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent import execute_tool


# ==========================================
# SUCCESSFUL TOOL EXECUTION
# ==========================================

def test_execute_calculator():
    decision = {
        "tool": "calculator",
        "arguments": {
            "expression": "45 * 9"
        }
    }

    result = execute_tool(decision)

    assert result["success"] is True
    assert result["result"] == 405


# ==========================================
# INVALID TOOL NAME
# ==========================================

def test_execute_unknown_tool():
    decision = {
        "tool": "unknown_tool",
        "arguments": {}
    }

    result = execute_tool(decision)

    assert result["success"] is False


# ==========================================
# MISSING REQUIRED ARGUMENT
# ==========================================

def test_execute_missing_argument():
    decision = {
        "tool": "calculator",
        "arguments": {}
    }

    result = execute_tool(decision)

    assert result["success"] is False


# ==========================================
# INVALID ARGUMENT TYPE
# ==========================================

def test_execute_invalid_argument_type():
    decision = {
        "tool": "calculator",
        "arguments": {
            "expression": 12345
        }
    }

    result = execute_tool(decision)

    assert result["success"] is False

    # ==========================================
# SECURITY TESTS
# ==========================================

def test_reject_non_dictionary_decision():

    result = execute_tool("calculator")

    assert result["success"] is False


def test_reject_unexpected_arguments():

    decision = {
        "tool": "calculator",
        "arguments": {
            "expression": "45 * 9",
            "extra": "malicious argument"
        }
    }

    result = execute_tool(decision)

    assert result["success"] is False


def test_reject_boolean_as_number():

    decision = {
        "tool": "unit_converter",
        "arguments": {
            "value": True,
            "from_unit": "km",
            "to_unit": "m"
        }
    }

    result = execute_tool(decision)

    assert result["success"] is False