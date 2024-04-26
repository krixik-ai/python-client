import sys
from io import StringIO
from functools import wraps


def capture_printed_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Redirect sys.stdout to a string buffer
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Call the decorated function
            result = func(*args, **kwargs)

            # Handle the case where the decorated function doesn't return anything
            if result is None:
                result = {}

            # Add the captured output to the result
            result["printed_output"] = sys.stdout.getvalue()

        finally:
            # Restore sys.stdout to its original value even if an exception occurs
            sys.stdout = original_stdout

        return result

    return wrapper
