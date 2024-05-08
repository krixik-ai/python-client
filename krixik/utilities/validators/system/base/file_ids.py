import re
from krixik.utilities.validators.system import MAX_FILE_ID_COUNT
from krixik.utilities.utilities import vprint

# define pattern for valid file id
file_id_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


def is_valid_uuid_string(input_string: str) -> bool:
    return bool(re.match(file_id_pattern, input_string))


def individual_file_id_checker(file_id: str) -> None:
    if file_id is not None:
        # check that file_id is a string
        if not isinstance(file_id, str):
            if file_id is None:
                raise ValueError("file_id must be input as an argument")
            else:
                raise TypeError("file_id must be input as a string")

        # check that file_id matches pattern
        res = is_valid_uuid_string(file_id)
        if res is False:
            raise TypeError(f"invalid file_id: a valid file_id is a string of length 36 with the following pattern: {file_id_pattern}")

        # check that file_id length is 36
        if len(file_id) != 36:
            raise TypeError(f"invalid file_id: length of this file_id is not 36 (it must be exactly 36 characters) - {file_id}")


def file_ids_checker(file_ids: list, verbose: bool = True) -> None:
    if file_ids is not None:
        # check that file_ids is a list of strings
        if not isinstance(file_ids, list):
            raise TypeError("file_ids is not a list")

        # check that file_ids is not empty
        if file_ids is not None:
            # check if length 0 list
            if len(file_ids) == 0:
                raise ValueError("file_ids is an empty list")

            # check if length greater than MAX_FILE_ID_COUNT
            if len(file_ids) > MAX_FILE_ID_COUNT:
                raise ValueError(f"file_ids contains more than {MAX_FILE_ID_COUNT} file_ids")

            # check each file_id for validity
            for file_id in file_ids:
                # check validity of file_id
                individual_file_id_checker(file_id)

            # check for duplicates
            if len(file_ids) != len(set(file_ids)):
                # find duplicates
                duplicates = []
                for file_id in file_ids:
                    if file_ids.count(file_id) > 1:
                        duplicates.append(file_id)

                # print error message
                vprint(
                    f"WARNING: file_ids contains duplicate entries - {duplicates}",
                    verbose=verbose,
                )
                vprint(
                    "INFO: You can remove duplicates by using Python's list(set()) function on your list of file_names",
                    verbose=verbose,
                )

        else:
            raise ValueError("file_ids is None")
