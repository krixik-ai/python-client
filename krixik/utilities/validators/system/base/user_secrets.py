import re


# define pattern for valid api_key
api_key_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


def is_valid_uuid_string(input_string: str) -> bool:
    return bool(re.match(api_key_pattern, input_string))


# define pattern for valid api_url
api_url_pattern = r"^(http|https)://[a-zA-Z0-9._%+-]+(?:\/[a-zA-Z0-9.-?%&=]*)?$"


def is_valid_api_url(input_string: str) -> bool:
    return bool(re.match(api_url_pattern, input_string))


def api_key_checker(api_key: str) -> None:
    # check if api_key is None
    if api_key is None:
        raise ValueError("you failed to authenticate - API key cannot be None")

    # type check api_key
    if not isinstance(api_key, str):
        raise TypeError("you failed to authenticate - invalid API key type - API key must be a string")

    # check that api_key matches pattern
    res = is_valid_uuid_string(api_key)
    if res is False:
        raise ValueError("invalid api_key: please check that this is a valid and correct api_key")


def api_url_checker(api_url: str) -> None:
    # check if api_url is None
    if api_url is None:
        raise ValueError("you failed to authenticate - API url cannot be None")

    # type check api_url
    if not isinstance(api_url, str):
        raise ValueError("you failed to authenticate - invalid API url type - API url must be a string")

    # check that api_url matches pattern
    res = is_valid_api_url(api_url)
    if res is False:
        raise ValueError("invalid api_url: please check that this is a valid and correct api_url")
