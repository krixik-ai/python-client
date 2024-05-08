import re

# define pattern for valid file id
id_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


def is_valid_uuid_string(input_string: str) -> bool:
    return bool(re.match(id_pattern, input_string))


def request_id_checker(request_id: str) -> None:
    if request_id is not None:
        # check that request_id is a string
        if not isinstance(request_id, str):
            if request_id is None:
                raise TypeError("request_id must be input as an argument")
            else:
                raise TypeError(f"Invalid request_id: not a string -  {request_id}")

        # check that request_id matches pattern
        res = is_valid_uuid_string(request_id)
        if res is False:
            raise ValueError(f"Invalid _id: a valid _id is a string of length 36 with the following pattern: {id_pattern}")

        # check that request_id length is 36
        if len(request_id) != 36:
            raise ValueError(f"Invalid _id: length of this _id is not 36 (it must be exactly 36 characters) - {request_id}")
