from krixik.utilities.validators.system.base.user_secrets import (
    api_key_checker,
    api_url_checker,
)
import pytest

test_failure_data = [
    (
        "c22a233c-3aee-499e-aacd-b5fae12e2f7e",
        "hi mom",
    ),
    (
        "not an api key",
        "https://4s1c32xo0f.execute-api.us-west-2.amazonaws.com/dev",
    ),
    (
        "not an api key",
        "not an api url",
    ),
]


def check_secrets(api_key, api_url):
    key_check = api_key_checker(api_key)
    url_check = api_url_checker(api_url)


@pytest.mark.parametrize("api_key, api_url", test_failure_data)
def test_failure(api_key, api_url):
    with pytest.raises(ValueError):
        check_secrets(api_key, api_url)
