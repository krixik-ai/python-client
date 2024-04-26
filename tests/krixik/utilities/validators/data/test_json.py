from krixik.utilities.validators.data.json import is_valid
from krixik.utilities.validators.data.json import is_size
from tests.krixik import json_files_path
SNIPPET_MAX_TOKEN_LENGTH = 255
SNIPPET_MAX_COUNT = 1000
import pytest


# test failure batch for is_valid
test_failures = [
    (json_files_path + "dne_file.json", FileNotFoundError),
    (json_files_path + "not_a_json_at_all.txt", ValueError),
    (json_files_path + "empty_dict.json", ValueError),
]


@pytest.mark.parametrize("local_file_path, expected_exception", test_failures)
def test_1(local_file_path, expected_exception):    
    with pytest.raises(expected_exception):
        is_valid(local_file_path)


# test failure batch for is_size
test_failures = [
    (json_files_path + "too_small.json", ValueError),
    (json_files_path + "too_large.json", ValueError),
    (json_files_path + "snippet_too_long.json", ValueError),
    (json_files_path + "snippet_too_many.json", ValueError),
]


@pytest.mark.parametrize("local_file_path, expected_exception", test_failures)
def test_2(local_file_path, expected_exception):
    with pytest.raises(expected_exception):
        is_size(
            local_file_path=local_file_path,
            snippet_max_token_count=SNIPPET_MAX_TOKEN_LENGTH,
            snippet_min_token_count=1,
            snippet_max_count=SNIPPET_MAX_COUNT,
            minimum_file_size=0.000001,
            maximum_file_size=3.000001,
        )


# test success batch for is_valid
test_successes = [
    json_files_path + "valid_1.json",
]


@pytest.mark.parametrize("local_file_path", test_successes)
def test_3(local_file_path):
    assert is_valid(local_file_path) is True
