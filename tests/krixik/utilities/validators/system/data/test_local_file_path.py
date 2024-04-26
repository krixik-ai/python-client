from krixik.utilities.validators.system.base.local_file_path import (
    local_file_path_checker,
)
from tests.krixik import text_files_path
import pytest

test_failure_data = [
    ["this cannot be a local file path"],
    "this is not a file path",
    "wow.abc",
    "audio_files/valid_1.mp3",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_failure(local_file_path):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)):
        local_file_path_checker(local_file_path)


test_success_data = [text_files_path + "my_life_and_work_short.txt"]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_success(local_file_path):
    assert local_file_path_checker(local_file_path) is None
