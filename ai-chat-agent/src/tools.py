
import ast
import operator
import math
from datetime import datetime
from collections import Counter
import re


# Supported mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


# Calculator tool
def calculator(expression):

    try:

        # Validate the expression
        if not isinstance(expression, str) or len(expression) > 100:
            raise ValueError("Expression is too long.")

        if not expression.strip():
            raise ValueError("Expression cannot be empty.")

        # Convert the expression into an AST
        tree = ast.parse(expression, mode="eval")

        # Limit the number of AST nodes
        if sum(1 for _ in ast.walk(tree)) > 50:
            raise ValueError("Expression is too complex.")

        # Evaluate only permitted mathematical operations
        def calculate(node):

            if isinstance(node, ast.Expression):
                return calculate(node.body)

            elif isinstance(node, ast.Constant):

                if type(node.value) in (int, float):

                    # Limit the size of numeric inputs
                    if isinstance(node.value, int) and node.value.bit_length() > 256:
                        raise ValueError("Number is too large.")

                    if isinstance(node.value, float):
                        if not math.isfinite(node.value) or abs(node.value) > 1e12:
                            raise ValueError("Number is outside the supported range.")

                    return node.value

                raise ValueError("Only numbers are allowed.")

            elif isinstance(node, ast.BinOp):

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported operation.")

                left = calculate(node.left)
                right = calculate(node.right)

                # Protect against excessive exponentiation
                if isinstance(node.op, ast.Pow):

                    if abs(right) > 8:
                        raise ValueError("Exponent is too large.")

                    if abs(left) > 1000000:
                        raise ValueError("Base is too large.")

                # Prevent division by zero
                if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
                    raise ValueError("Division by zero is not allowed.")

                result = operation(left, right)

                # Limit integer result size
                if isinstance(result, int) and result.bit_length() > 256:
                    raise ValueError("Result is too large.")

                # Check floating-point results
                if isinstance(result, float):
                    if not math.isfinite(result) or abs(result) > 1e100:
                        raise ValueError("Result is outside the supported range.")

                return result

            elif isinstance(node, ast.UnaryOp):

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported operation.")

                return operation(calculate(node.operand))

            else:
                raise ValueError("Invalid mathematical expression.")

        result = calculate(tree)

        return result

    except (
        SyntaxError,
        ValueError,
        TypeError,
        OverflowError,
        ZeroDivisionError
    ):
        return "Invalid or unsupported mathematical expression."



# DATE AND TIME TOOL

def date_and_time():

    # Get the current local date and time
    current_time = datetime.now().astimezone()

    # Format the date and time
    formatted_time = current_time.strftime(
        "%A, %d %B %Y, %I:%M:%S %p"
    )

    return formatted_time


# ==========================================
# WORD COUNTER TOOL
# ==========================================

def word_counter(text):

    if not isinstance(text, str):
        raise TypeError("Input must be text.")

    words = text.split()

    return {
        "words": len(words),
        "characters": len(text),
        "characters_without_spaces": len(text.replace(" ", ""))
    }


# ==========================================
# TEXT ANALYZER TOOL
# ==========================================

def text_analyzer(text):

    if not isinstance(text, str):
        raise TypeError("Input must be text.")

    words = re.findall(r"\b[\w']+\b", text.lower())

    sentences = re.findall(r"[.!?]+", text)

    paragraphs = [
        paragraph for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    common_words = Counter(words).most_common(5)

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "most_common_words": common_words
    }


# ==========================================
# UNIT CONVERTER TOOL
# ==========================================

def unit_converter(value, from_unit, to_unit):

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("Value must be a number.")

    units = {
        "m": ("length", 1),
        "km": ("length", 1000),
        "cm": ("length", 0.01),
        "mm": ("length", 0.001),
        "ft": ("length", 0.3048),
        "in": ("length", 0.0254),
        "mi": ("length", 1609.344),

        "kg": ("weight", 1),
        "g": ("weight", 0.001),
        "mg": ("weight", 0.000001),
        "lb": ("weight", 0.45359237),
        "oz": ("weight", 0.028349523125)
    }

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in units or to_unit not in units:
        raise ValueError("Unsupported unit.")

    if units[from_unit][0] != units[to_unit][0]:
        raise ValueError("Cannot convert between different unit categories.")

    base_value = value * units[from_unit][1]

    converted_value = base_value / units[to_unit][1]

    return {
        "original_value": value,
        "from_unit": from_unit,
        "converted_value": round(converted_value, 6),
        "to_unit": to_unit
    }


# ==========================================
# TOOL REGISTRY
# ==========================================

TOOLS = {

    "calculator": {
        "function": calculator,
        "description": "Performs mathematical calculations.",
        "parameters": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression.",
                "required": True
            }
        }
    },

    "date_and_time": {
        "function": date_and_time,
        "description": "Returns the current date and time.",
        "parameters": {}
    },

    "word_counter": {
        "function": word_counter,
        "description": "Counts words and characters in text.",
        "parameters": {
            "text": {
                "type": "string",
                "description": "Text to count.",
                "required": True
            }
        }
    },

    "text_analyzer": {
        "function": text_analyzer,
        "description": "Analyses text and identifies common words, sentences and paragraphs.",
        "parameters": {
            "text": {
                "type": "string",
                "description": "Text to analyse.",
                "required": True
            }
        }
    },

    "unit_converter": {
        "function": unit_converter,
        "description": "Converts supported length and weight units.",
        "parameters": {
            "value": {
                "type": "number",
                "description": "Numeric value to convert.",
                "required": True
            },
            "from_unit": {
                "type": "string",
                "description": "Original unit, such as km or kg.",
                "required": True
            },
            "to_unit": {
                "type": "string",
                "description": "Target unit, such as m or g.",
                "required": True
            }
        }
    }
}
