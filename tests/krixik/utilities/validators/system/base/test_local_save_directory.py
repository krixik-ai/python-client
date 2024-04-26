from krixik.utilities.validators.system.base.local_save_directory import (
    local_save_directory_checker,
)
from tests.krixik import text_files_path
import pytest


test_failure_data = [
    [],
    {},
    1,
    "/a/path/to/nowhere",
    "",
    " ",
    text_files_path[1:],
    text_files_path + "/*",
]


@pytest.mark.parametrize("local_save_directory", test_failure_data)
def test_failure(local_save_directory):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)) as excinfo:
        local_save_directory_checker(local_save_directory)


test_success_data = [text_files_path]


@pytest.mark.parametrize("local_save_directory", test_success_data)
def test_success(local_save_directory):
    assert local_save_directory_checker(local_save_directory) is None
