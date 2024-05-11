import re
from collections import Counter
from krixik.utilities.validators import MAX_CLEAN_OPTIONS_COUNT
from krixik.utilities.validators import (
    CLEAN_OPTION_VALUE_MAX_LENGTH,
)


# validity pattern for clean_option key and value
tags_pattern = r'^[a-zA-Z0-9\s\-_.,;\'"!?]*$'


def contains_only_alphanumeric(input_string: str) -> bool:
    return bool(re.match(tags_pattern, input_string))


# check individual clean option
def individual_clean_option_checker(key: str, value: str) -> None:
    # check that key is a string
    if not isinstance(key, str):
        raise TypeError(f"invalid clean_option key: not a string - {key}")

    # check that key length is greater than 0
    if len(key) != 1:
        raise ValueError(f"invalid clean_option key: length is not equal to 1 - {key}")

    # check that key is not equal to ' '
    if key == " ":
        raise ValueError(f"invalid clean_option key: key cannot be a space - {key}")

    # check that value is a string
    if not isinstance(value, str):
        raise TypeError(f"invalid clean_option value: not a string - {value}")

    # check that value length is less than CLEAN_OPTION_VALUE_MAX_LENGTH
    if len(value) > CLEAN_OPTION_VALUE_MAX_LENGTH:
        raise ValueError(f"invalid clean_option value: length is greater than 32 (current maximum length allowable) - {value}")

    # check that value contains only alphanumeric and alphanumeric characters
    res = contains_only_alphanumeric(value)
    if res is False:
        raise ValueError(f"invalid clean_option value: please check that it contains only basic alphanumeric characters or punctuation - {value}")

    # check that key is not equal to value
    if key == value:
        raise ValueError(f"invalid clean_option: key and value cannot be the same - {key} and {value}")


# check clean_options
def clean_options_checker(clean_options: dict) -> None:
    if clean_options is not None:
        # check that clean_options is a dict
        if not isinstance(clean_options, dict):
            raise TypeError("clean_options is not a dict")

        # if dict is empty, raise error
        if len(clean_options) == 0:
            raise ValueError("invalid clean_options: empty dict provided, you must provide at least one clean_option")

        # check that clean_options is less or equal to MAX_CLEAN_OPTIONS_COUNT
        if len(clean_options) > MAX_CLEAN_OPTIONS_COUNT:
            raise ValueError(
                f"invalid clean_options: more than {MAX_CLEAN_OPTIONS_COUNT} clean_options provided, you can have a maximum of {MAX_CLEAN_OPTIONS_COUNT}"
            )

        # loop over keys / values and check for validity
        keys = list(clean_options.keys())
        values = list(clean_options.values())
        for key, value in zip(keys, values):
            individual_clean_option_checker(key, value)

        # check that keys and values share no common elements
        common_elements = set(keys) & set(values)
        if len(common_elements) > 0:
            raise ValueError(f"invalid clean_options: keys and values cannot share common elements - {common_elements}")

        # check for duplicates - print duplicates
        c = Counter(keys)
        invalid_keys = []
        for item in c.items():
            key = item[0]
            value = item[1]
            if value > 1:
                invalid_keys.append(key)

        # print invalid keys
        if len(invalid_keys) > 0:
            raise ValueError(f"invalid clean_options: duplicate keys found: {invalid_keys}")
