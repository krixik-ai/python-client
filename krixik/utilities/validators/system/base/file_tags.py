import re
from krixik.utilities.validators.system import (
    TAGS_COUNT_MAX,
    TAG_KEY_LENGTH_MAX,
    TAG_VALUE_LENGTH_MAX,
)

# validity pattern for file tags key and value
tags_pattern = r"^[a-zA-Z0-9\s\-_]*$"


def contains_only_alphanumeric_and_alphanumeric(input_string: str) -> bool:
    return bool(re.match(tags_pattern, input_string))


# check individual file tag
def individual_file_tag_checker(file_tag: dict, phase: str = "other") -> None:
    # check that file_tag is a dict
    if not isinstance(file_tag, dict):
        raise TypeError(f"file_tag must be input as a dictionary - {file_tag}")

    # check that file_tag is a dictionary with only one key-value pair
    if len(file_tag) != 1:
        raise ValueError(f"file_tag must be a dictionary with only one key-value pair - {file_tag}")

    # check key and value of file_tag to be valid strings
    key = list(file_tag.keys())[0]
    value = file_tag[key]

    # check that key is a string
    if not isinstance(key, str):
        raise TypeError(f"invalid file_tag key: not a string - {key}")

    # check that key length is greater than 0
    if len(key) == 0:
        raise ValueError(f"invalid file_tag key: length is 0 - {key}")

    # check that key length is less than 32
    if len(key) > TAG_KEY_LENGTH_MAX:
        raise ValueError(f"invalid file_tag key: length is greater than {TAG_KEY_LENGTH_MAX} (current maximum length allowable) - {key}")

    # check that key contains only alphanumeric and alphanumeric characters
    res = contains_only_alphanumeric_and_alphanumeric(key)
    if res is False:
        raise ValueError(f"invalid file_tag key: {key} - please check that it contains only alphanumeric and alphanumeric characters")

    # check that value is a string
    if not isinstance(value, str):
        raise ValueError(f"invalid file_tag value: not a string - {value}")

    # check that value length is greater than 0
    if len(value) == 0:
        raise ValueError(f"invalid file_tag value: length is 0 - {value}")

    # check that value length is less than 32
    if len(value) > TAG_VALUE_LENGTH_MAX:
        raise ValueError(f"invalid file_tag value: length is greater than {TAG_VALUE_LENGTH_MAX} (current maximum length allowable) - {value}")

    # if phase is process do not allow wildcard
    if phase == "process":
        if value == "*":
            raise ValueError(
                f"invalid file_tag value: {value} - please check that it is either a wildcard (*) or contains only alphanumeric and alphanumeric characters"
            )

    # check that value contains only alphanumeric and alphanumeric characters
    if value != "*":
        res = contains_only_alphanumeric_and_alphanumeric(value)
        if res is False:
            raise ValueError(f"invalid file_tag value: {value} - please check that it contains only alphanumeric and alphanumeric characters")


def lower_case_file_tags(file_tags: list) -> list:
    # lower case all tags
    lower_case_tags = []
    for file_tag in file_tags:
        key = list(file_tag.keys())[0]
        value = file_tag[key]
        lower_file_tag = {key.lower(): value.lower()}
        lower_case_tags.append(lower_file_tag)
    return lower_case_tags


def file_tags_checker(file_tags: list, phase: str = "other") -> None:
    if file_tags is not None:
        # check that file_tags is a list
        if not isinstance(file_tags, list):
            raise TypeError("file_tags is not a list")

        # check that file_tags is not empty
        lower_case_tags = []
        if file_tags is not None:
            # loop over each tag in file_tags and check for validity
            tag_count = 0
            for file_tag in file_tags:
                # check that tag_count is less or equal to 20
                if tag_count > TAGS_COUNT_MAX - 1:
                    raise ValueError(
                        f"Invalid file_tags: {file_tags} - more than {TAGS_COUNT_MAX} tags provided, you can have a maximum of {TAGS_COUNT_MAX} tags"
                    )

                # type check each file tag
                individual_file_tag_checker(file_tag, phase=phase)

                # increment tag_count
                tag_count += 1

            # lower case tags
            lower_case_tags = lower_case_file_tags(file_tags)

            # check for duplicate dicts in lower_case_file_tags
            if len(lower_case_tags) != len(set(map(lambda x: frozenset(x.items()), lower_case_tags))):
                # determine duplicates
                duplicates = []
                seen = set()
                for tag in lower_case_tags:
                    if frozenset(tag.items()) in seen:
                        duplicates.append(tag)
                    else:
                        seen.add(frozenset(tag.items()))
                raise ValueError(f"file_tags contains duplicate key-value pairs: {duplicates}")
        else:
            raise ValueError("file_tags is None")
