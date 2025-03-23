def add(a: int | float, b: int | float) -> float:
    """Add two numbers together.

    Args:
        a: First number (int or float).
        b: Second number (int or float).

    Returns:
        The result of a + b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("add: both arguments must be int or float")
    return a + b

def subtract(a: int | float, b: int | float) -> float:
    """Subtract the second number from the first.

    Args:
        a: First number (int or float).
        b: Second number (int or float).

    Returns:
        The result of a - b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("subtract: both arguments must be int or float")
    return a - b

def multiply(a: int | float, b: int | float) -> float:
    """Multiply two numbers.

    Args:
        a: First number (int or float).
        b: Second number (int or float).

    Returns:
        The result of a * b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("multiply: both arguments must be int or float")
    return a * b

def divide(a: int | float, b: int | float) -> float:
    """Divide the first number by the second.

    Args:
        a: Numerator (int or float).
        b: Denominator (int or float).

    Returns:
        The result of a / b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("divide: both arguments must be int or float")
    return a / b

def power(a: int | float, b: int | float) -> float:
    """Raise the first number to the power of the second.

    Args:
        a: Base number (int or float).
        b: Exponent (int or float).

    Returns:
        The result of a raised to the power of b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("power: both arguments must be int or float")
    return a ** b

def modulo(a: int | float, b: int | float) -> float:
    """Return the remainder of the first number divided by the second.

    Args:
        a: Dividend (int or float).
        b: Divisor (int or float).

    Returns:
        The remainder of a divided by b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("modulo: both arguments must be int or float")
    return a % b

def absolute(a: int | float) -> float:
    """Return the absolute value of a number.

    Args:
        a: A number (int or float).

    Returns:
        The absolute value of a.
    """
    if not isinstance(a, (int, float)):
        raise TypeError("absolute: argument must be int or float")
    return abs(a)

def logarithm(a: int | float, base: int | float = 10) -> float:
    """Return the logarithm of a number with the given base.

    Args:
        a: The number to take the logarithm of (int or float).
        base: The logarithmic base (int or float), default is 10.

    Returns:
        The logarithm of a with the given base.
    """
    import math
    if not isinstance(a, (int, float)) or not isinstance(base, (int, float)):
        raise TypeError("logarithm: both arguments must be int or float")
    return math.log(a, base)

def square_root(a: int | float) -> float:
    """Return the square root of a number.

    Args:
        a: A number (int or float).

    Returns:
        The square root of a.
    """
    import math
    if not isinstance(a, (int, float)):
        raise TypeError("square_root: argument must be int or float")
    return math.sqrt(a)

# Tool lists for clean reuse
basic_tools = [
    {"name": "add", "func": add},
    {"name": "subtract", "func": subtract},
    {"name": "multiply", "func": multiply},
    {"name": "divide", "func": divide},
]

extended_tools = [
    {"name": "add", "func": add},
    {"name": "subtract", "func": subtract},
    {"name": "multiply", "func": multiply},
    {"name": "divide", "func": divide},
    {"name": "power", "func": power},
    {"name": "modulo", "func": modulo},
    {"name": "absolute", "func": absolute},
    {"name": "logarithm", "func": logarithm},
    {"name": "square_root", "func": square_root},
]