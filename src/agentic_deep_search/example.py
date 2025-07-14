"""Example module to demonstrate ruff formatting."""


def poorly_formatted_function(x, y, z):
    # This function has poor formatting
    if x > 0 and y < 10:
        result = x + y * z
        return result
    else:
        return None


class BadlyFormattedClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return {"name": self.name, "age": self.age}


# Long line that exceeds the line length limit and should be wrapped by ruff when formatting
very_long_variable_name_that_makes_this_line_too_long = (
    "This is a very long string that should be wrapped"
)

# Unused import (should be caught by ruff)
