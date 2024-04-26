from krixik.utilities.validators.system.base.local_file_path import (
    local_file_path_checker,
)
from tests.krixik import text_files_path
import pytest


test_failure_data = [
    [],
    {},
    1,
    "/a/path/to/nowhere",
    "s" * 1000,
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_failure(local_file_path):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)):
        local_file_path_checker(local_file_path)


test_success_data = [text_files_path]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_success(local_file_path):
    assert local_file_path_checker(local_file_path) is None
