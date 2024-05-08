import inspect
from typing import Any
from krixik.utilities.converters.default_clean_options import acceptable_chars


class classproperty:
    def __init__(self, func):
        self.fget = func

    def __get__(self, instance, owner):
        return self.fget(owner)


def invalid_char_check(line: str) -> set[str]:
    invalid_char: set[str] = set()
    for char in line:
        if ord(char) > 128 and char not in acceptable_chars:
            invalid_char.add(char)
    return invalid_char


def vprint(message: str, *, verbose: bool = False) -> None:
    # check that message is string
    if not isinstance(message, str):
        raise TypeError("message must be a string")

    # check that verbose is boolean
    if not isinstance(verbose, bool):
        raise TypeError("verbose must be a boolean")

    if verbose:
        print(message)


def get_input(
    input_name: str | None,
    signature: inspect.Signature,
    kwargs: dict[str, str],
    default_value: Any = None,
) -> Any:
    inspect._empty
    input_value = signature.parameters.get(input_name).default if input_name in signature.parameters else None
    if input_value is inspect._empty:
        input_value = None
    if input_name in list(kwargs.keys()):
        input_value = kwargs[input_name]
    if input_value is None:
        input_value = default_value
    return input_value


def load_docstring(file_path):
    with open(file_path, "r") as file:
        docstring = file.read()
    return docstring
