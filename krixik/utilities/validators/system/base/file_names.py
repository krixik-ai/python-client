import copy
import re
from krixik.utilities.utilities import vprint
from krixik.utilities.validators.system import (
    MAX_FILE_NAME_LENGTH,
    MAX_FILE_NAME_COUNT,
)

# define pattern for valid file names
file_names_pattern = r"^[a-zA-Z0-9 _,.-]+(\.[a-zA-Z0-9]+)?$"


def is_valid_file_name(file_name: str) -> bool:
    return bool(re.match(file_names_pattern, file_name))


# individual file_name checker
def individual_file_name_checker(file_name: str, valid_extensions: list = [], phase: str = "other") -> None:
    if file_name is not None:
        # check that file_name is a string
        if not isinstance(file_name, str):
            raise TypeError("file_name must be input as a string")

        # check that file_name length is greater than 0
        if len(file_name) == 0:
            raise ValueError("invalid file_name: length is 0")

        # check that file_name length is less than 64
        if len(file_name) > MAX_FILE_NAME_LENGTH:
            raise ValueError(
                f"invalid file_name: length is greater than 64 (current maximum length allowable) - {file_name} - length is {len(file_name)}"
            )

        # check for single asterisk
        if file_name == "*":
            raise ValueError("invalid file_name: cannot be '*'")

        # check that file_name is a valid file name
        if phase == "process":
            res = is_valid_file_name(file_name)
            if res is False:
                raise ValueError(
                    f"invalid file_name: please check that it contains only alphanumeric, alphanumeric, '_', or '-', characters - {file_name}"
                )

            # check if * is in file_name
            if "*" in file_name:
                raise ValueError(f"invalid file_name for process: please check that it does not contain any '*' characters - {file_name}")

            # check that file_name ends with an valid_extensions
            if "." + file_name.split(".")[-1] not in valid_extensions:
                raise ValueError(
                    f"invalid file_name: please check that it ends with an allowed extension - {file_name} - allowed extensions: {valid_extensions}"
                )

        if phase != "process":
            # check if input file_name begins or ends with '*'
            test_file_name = copy.deepcopy(file_name)

            # check for **
            if "**" in test_file_name:
                raise ValueError(f"invalid file_name: please check that it does not contain any '**' characters - {file_name}")

            # check for ***
            if "***" in test_file_name:
                raise ValueError(f"invalid file_name: please check that it does not contain any '***' characters - {file_name}")

            # check if input file_name begins or ends with '*'
            test_file_name = copy.deepcopy(file_name)

            if file_name[0] == "*":
                test_file_name = test_file_name[1:]

            if file_name[-1] == "*":
                test_file_name = test_file_name[:-1]
            else:
                # extension must fall into valid_extensions
                if "." + file_name.split(".")[-1] not in valid_extensions:
                    raise ValueError(
                        f"invalid file_name: please check that it ends with an allowed extension - {file_name} - allowed extensions: {valid_extensions}"
                    )

            # split on possible extension
            non_extension = test_file_name.split(".")[0]

            if len(non_extension) > 0:
                # test for validity of file_name
                res = is_valid_file_name(non_extension)
                if res is False:
                    raise ValueError(
                        f"invalid file_name: please check that the core (excluding an optional single '*' at the beginning and/or end) of this file_name contains only basic alphanumeric, underscore, and/or hyphen characters - your input file_name: {file_name}"
                    )


# check file names
def file_names_checker(
    file_names: list,
    phase: str = "other",
    valid_extensions: list = [],
    verbose: bool = True,
) -> None:
    if file_names is not None:
        # check that file_names is a list
        if not isinstance(file_names, list):
            raise TypeError("file_names is not a list")

        # check that file_names is not empty
        if len(file_names) == 0:
            raise ValueError("file_names is empty")

        # check that file_names is not too long
        if len(file_names) > MAX_FILE_NAME_COUNT:
            raise ValueError(f"file_names contains more than {MAX_FILE_NAME_COUNT} file_names")

        # check that file_names is not empty
        if file_names is not None:
            # check that all file_names are valid file names
            for file_name in file_names:
                # check validity of file_name
                individual_file_name_checker(file_name, valid_extensions, phase=phase)

            # check for duplicates
            if len(file_names) != len(set(file_names)):
                # find duplicates
                duplicates = []
                for file_name in file_names:
                    if file_names.count(file_name) > 1:
                        duplicates.append(file_name)

                # print error message
                vprint(
                    f"WARNING: file_names contains duplicate entries - {duplicates}",
                    verbose=verbose,
                )
                vprint(
                    "INFO: You can remove duplicates by using Python's list(set()) function on your list of file_names",
                    verbose=verbose,
                )
        else:
            raise ValueError("file_names is None")
