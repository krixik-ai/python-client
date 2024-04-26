from krixik.utilities.validators.data.npy import is_valid
from krixik.utilities.validators.data.npy import is_size
from tests.krixik import npy_files_path, json_files_path
import pytest


# test failure batch for is_valid
test_failures = [
    (npy_files_path + "dne_file.npy", FileNotFoundError),
    (json_files_path + "valid_1.json", ValueError),
]


@pytest.mark.parametrize("local_file_path, expected_exception", test_failures)
def test_1(local_file_path, expected_exception):
    with pytest.raises(expected_exception):
        is_valid(local_file_path)


# test success batch for is_valid
test_successes = [
    npy_files_path + "valid_1.npy",
]


@pytest.mark.parametrize("local_file_path", test_successes)
def test_3(local_file_path):
    assert is_valid(local_file_path) is None
