from krixik.utilities.validators.system.base.file_description import (
    file_description_checker,
)
from krixik.utilities.validators.system import FILE_DESCRIPTION_MAX_LENGTH
import pytest

test_failure_data = [
    "".join(["s" for i in range(300)]),
    ["i am a list"],
    1,
    "然後將醬油放入麵包籃中盡情歡樂",
    "a" * (FILE_DESCRIPTION_MAX_LENGTH + 1),
    [],
    {},
]


@pytest.mark.parametrize("file_description", test_failure_data)
def test_failure(file_description):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        file_description_checker(file_description)


test_success_data = ["hello world", ""]


@pytest.mark.parametrize("file_description", test_success_data)
def test_success(file_description):
    assert file_description_checker(file_description) is None
