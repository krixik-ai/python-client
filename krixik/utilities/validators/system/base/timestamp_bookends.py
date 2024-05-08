import copy
from datetime import datetime, timezone
from krixik.utilities.utilities import vprint

# valid timestamp formats
timestamp_valid_formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]


# check that timestamp represents a valid date
def is_valid_timestamp(timestamp: str) -> None:
    for format_str in timestamp_valid_formats:
        try:
            datetime.strptime(timestamp, format_str)
        except ValueError:
            raise ValueError(f"{timestamp} must be a valid date but was given as {timestamp}")


def numerical_timestamp_checker(timestamp_int: int, timestamp_name: str) -> None:
    if not isinstance(timestamp_int, int):
        raise TypeError(f"{timestamp_name} must be an integer but was given as {timestamp_int}")
    if timestamp_int < 0:
        raise ValueError(f"{timestamp_name} must be a positive integer but was given as {timestamp_int}")


def string_timestamp_to_int(timestamp_str: str, timestamp_name: str) -> int | None:
    dt_object = None
    dt_object_utc = None
    dt_check = 0
    for format in timestamp_valid_formats:
        try:
            # Attempt to parse the timestamp string into a datetime object
            dt_object = datetime.strptime(timestamp_str, format)

            # Convert the datetime object to a UTC datetime object
            dt_object_utc = dt_object.replace(tzinfo=timezone.utc)

            dt_check += 1
            break
        except ValueError:
            pass
            # raise ValueError(f'{timestamp_name} must be in format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS but was given as {timestamp_str}')

    if dt_check == 0:
        raise ValueError(f"{timestamp_name} must be in format -- YYYY-MM-DD -- or -- YYYY-MM-DD HH:MM:SS -- but was given as {timestamp_str}")

    # Convert the datetime object to a Unix timestamp (seconds since epoch)
    if dt_object_utc is not None:
        timestamp_int_utc = int(dt_object_utc.timestamp())
        return timestamp_int_utc


def is_valid_format(timestamp_str: str, timestamp_name: str) -> None:
    # check if timestamp is in correct format
    dt_check = 0
    for format in timestamp_valid_formats:
        try:
            # Attempt to parse the timestamp string
            datetime.strptime(timestamp_str, format)
            dt_check += 1
        except ValueError:
            pass
            # raise ValueError(f'{timestamp_name} must be in format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS but was given as {timestamp_str}')
    if dt_check == 0:
        raise ValueError(f"{timestamp_name} must be in format YYYY-MM-DD or YYYY-MM-DD HH:MM:SS but was given as {timestamp_str}")


def is_stump(timestamp_str: str, start_end: str | None = None, verbose: bool = False) -> str:
    try:  # if timestamp_str is format '%Y-%m-%d' then add '23:59:59' to the end of the timestamp
        datetime.strptime(timestamp_str, "%Y-%m-%d")
        og_timestamp_str = copy.deepcopy(timestamp_str)
        if start_end == "start":
            timestamp_str = timestamp_str + " 00:00:00"
        if start_end == "end":
            timestamp_str = timestamp_str + " 23:59:59"
        vprint(
            f"INFO: Interpreting {og_timestamp_str} as {timestamp_str} to ensure temporally inclusive query",
            verbose=verbose,
        )
        return timestamp_str
    except ValueError:
        return timestamp_str


def is_after_bot(timestamp: str, timestamp_name: str) -> None:
    # check that timestamp occurs after 2023-01-01
    if timestamp < "2023-01-01":
        raise ValueError(f"{timestamp_name} must be after 2023-01-01 but was given as {timestamp}")

    # check if timestamp occurs after the year 9999
    if timestamp > "9999-12-31":
        raise ValueError(f"{timestamp_name} must be before 9999-12-31 but was given as {timestamp}")


def timestamp_checker(timestamp: str, timestamp_name: str, start_end: str, verbose: bool = False) -> int | None:
    # check if timestamp is a string
    if not isinstance(timestamp, str):
        raise TypeError(f"{timestamp_name} must be a string but was given as {timestamp}")

    # check if timestamp is in correct format
    is_valid_format(timestamp, timestamp_name)

    # check if stump
    timestamp = is_stump(timestamp, start_end=start_end, verbose=verbose)

    # check that timestamp occurs after 2023-01-01
    is_after_bot(timestamp, timestamp_name)

    # convert timestamp to int
    timestamp_int = string_timestamp_to_int(timestamp, timestamp_name)

    # double check timestamp_int is a positive integer
    if timestamp_int is not None:
        numerical_timestamp_checker(timestamp_int, timestamp_name)
        return timestamp_int


def timestamp_bookends_checker(
    created_at_start: str | None = None,
    created_at_end: str | None = None,
    last_updated_start: str | None = None,
    last_updated_end: str | None = None,
    verbose: bool = False,
) -> None:
    # make copy for reference messaging
    og_created_at_start = copy.deepcopy(created_at_start)
    og_created_at_end = copy.deepcopy(created_at_end)
    og_last_updated_start = copy.deepcopy(last_updated_start)
    og_last_updated_end = copy.deepcopy(last_updated_end)

    # check each bookend
    created_at_start_int = None
    created_at_end_int = None
    last_updated_start_int = None
    last_updated_end_int = None
    if created_at_start is not None:
        created_at_start_int = timestamp_checker(created_at_start, "created_at_start", start_end="start", verbose=verbose)

    if created_at_end is not None:
        created_at_end_int = timestamp_checker(created_at_end, "created_at_end", start_end="end", verbose=verbose)

    if last_updated_start is not None:
        last_updated_start_int = timestamp_checker(last_updated_start, "last_updated_start", start_end="start", verbose=verbose)

    if last_updated_end is not None:
        last_updated_end_int = timestamp_checker(last_updated_end, "last_updated_end", start_end="end", verbose=verbose)

    # check comparisons between bookends
    if created_at_start_int is not None and created_at_end_int is not None:
        if created_at_start_int > created_at_end_int:
            raise ValueError(f"created_at_start {og_created_at_start} must occur before created_at_end {og_created_at_end}.")

    if last_updated_start_int is not None and last_updated_end_int is not None:
        if last_updated_start_int > last_updated_end_int:
            raise ValueError(f"last_updated_start {og_last_updated_start} must occur before last_updated_end {og_last_updated_end}.")


def convert_timestamps(
    created_at_start: str | None,
    created_at_end: str | None,
    last_updated_start: str | None,
    last_updated_end: str | None,
) -> tuple[int | None, int | None, int | None, int | None]:
    created_at_start_int = None
    created_at_end_int = None
    last_updated_start_int = None
    last_updated_end_int = None
    if created_at_start is not None:
        created_at_start = is_stump(created_at_start, "start", verbose=False)
        created_at_start_int = string_timestamp_to_int(created_at_start, "created_at_start")
    if last_updated_start is not None:
        last_updated_start = is_stump(last_updated_start, "start", verbose=False)
        last_updated_start_int = string_timestamp_to_int(last_updated_start, "last_updated_start")
    if created_at_end is not None:
        created_at_end = is_stump(created_at_end, "end", verbose=False)
        created_at_end_int = string_timestamp_to_int(created_at_end, "created_at_end")
    if last_updated_end is not None:
        last_updated_end = is_stump(last_updated_end, "end", verbose=False)
        last_updated_end_int = string_timestamp_to_int(last_updated_end, "last_updated_end")
    return (
        created_at_start_int,
        created_at_end_int,
        last_updated_start_int,
        last_updated_end_int,
    )
