from krixik.utilities.validators.data.audio import is_valid
from krixik.utilities.validators.data.audio import is_size
from tests.krixik import audio_files_path
import pytest

# first - check is_valid
test_failure_data = [
    audio_files_path + "invalid_1.mp3",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_1(local_file_path):
    """ failed input is not a proper mp3 """
    with pytest.raises((ValueError, TypeError)):
        is_valid(local_file_path=local_file_path)


test_success_data = [
    audio_files_path + "valid_1.mp3",
]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_2(local_file_path):
    """ success input is a proper mp3 """
    assert is_valid(local_file_path=local_file_path) is None


# second - check is_size
test_failure_data = [
    # audio_files_path + "Empty McFile.mp3",  # 0 bytes
    audio_files_path + "too_long.mp3",  # > 3mb
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_3(local_file_path):
    """ size tests for too large/small """
    with pytest.raises((ValueError, TypeError), match=r".*current maximum size allowable\.*"):
        is_size(
            local_file_path=local_file_path,
            minimum_seconds=3,
            maximum_seconds=180,
            minimum_file_size=0.000001,
            maximum_file_size=3.0,
        )


test_success_data = [
    audio_files_path + "valid_1.mp3",
]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_4(local_file_path):
    """ size test success """
    assert (
        is_size(
            local_file_path=local_file_path,
            minimum_seconds=3,
            maximum_seconds=180,
            minimum_file_size=0.000001,
            maximum_file_size=3.0,
        )
        is None
    )


