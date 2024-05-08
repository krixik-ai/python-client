import re
from krixik.utilities.validators.system import FILE_DESCRIPTION_MAX_LENGTH

# validity pattern for file tags key and value
tags_pattern = r'^[a-zA-Z0-9\s\-_.,;\'"!?]*$'


def contains_only_alphanumeric_and_alphanumeric(input_string: str) -> bool:
    return bool(re.match(tags_pattern, input_string))


def file_description_checker(file_description: str) -> None:
    if file_description is not None:
        # check that file_description is a string
        if not isinstance(file_description, str):
            raise TypeError(f"invalid file description: not a string - {file_description}")

        # check that file_description length is less than FILE_DESCRIPTION_MAX_LENGTH
        if len(file_description) > FILE_DESCRIPTION_MAX_LENGTH:
            raise ValueError(
                f"invalid file description: length is greater than 256 characters (current maximum length allowable) - {file_description}"
            )

        # check that file_description contains only alphanumeric and alphanumeric characters
        if not contains_only_alphanumeric_and_alphanumeric(file_description):
            raise TypeError(f"invalid file description: contains non-alphanumeric/punctuation characters - {file_description}")
