from krixik.utilities.validators.system.base.clean_options import (
    clean_options_checker,
)
from krixik.utilities.validators import MAX_CLEAN_OPTIONS_COUNT
from krixik.utilities.validators import (
    CLEAN_OPTION_VALUE_MAX_LENGTH,
)
import pytest

test_failure_data = [
    "",
    " ",
    [],
    {},
    1,
    {"a": "a"},
    {"áa": "a"},
    {"á": "a" * (CLEAN_OPTION_VALUE_MAX_LENGTH + 1)},
    {"á": "é"},
    {" ": "a"},
    [{"á": "a"} for i in range(MAX_CLEAN_OPTIONS_COUNT + 1)],
]


@pytest.mark.parametrize("clean_options", test_failure_data)
def test_failure(clean_options):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        clean_options_checker(clean_options)


test_success_data = [
    {"á": "a"},
]


@pytest.mark.parametrize("clean_options", test_success_data)
def test_success(clean_options):
    assert clean_options_checker(clean_options) is None
