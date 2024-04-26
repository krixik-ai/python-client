from krixik.utilities.validators.system.base.max_files import max_files_checker
from krixik.utilities.validators.system import MAX_FILES_COUNT
import pytest

test_failure_data = [
    "hi",
    0,
    -1,
    [],
    {},
    1.5,
    True,
    False,
    MAX_FILES_COUNT + 1,
]


@pytest.mark.parametrize("max_files", test_failure_data)
def test_failure(max_files):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        max_files_checker(max_files)


test_success_data = [
    MAX_FILES_COUNT,
]


@pytest.mark.parametrize("max_files", test_success_data)
def test_success(max_files):
    assert max_files_checker(max_files) is None
