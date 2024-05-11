from krixik.utilities.converters.video_to_audio import (
    convert,
)
from krixik.utilities.validators.data.audio import is_valid
from tests.krixik import video_files_path, audio_files_path
import pytest

valid_local_file_path = video_files_path + "valid_1.mp4"
valid_local_save_directory = audio_files_path


test_failure_data = [
    (None, None),
]


@pytest.mark.parametrize("local_file_path, local_save_directory", test_failure_data)
def test_1(local_file_path, local_save_directory):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)):
        convert(
            local_file_path=local_file_path, local_save_directory=local_save_directory
        )


test_success_data = [
    (
        valid_local_file_path,
        valid_local_save_directory,
    ),  # local_save_directory provided
]


@pytest.mark.parametrize("local_file_path, local_save_directory", test_success_data)
def test_2(local_file_path, local_save_directory):
    assert (
        convert(
            local_file_path=local_file_path, local_save_directory=local_save_directory
        )
        is not None
    )


def test_delete_on_failure():
    # create polluted characters that will be recursively enlarged in test file
    valid_local_file_path = video_files_path + "/" + "test_video_3.mp4"
    valid_local_save_directory = audio_files_path

    with pytest.raises((ValueError, TypeError, FileNotFoundError)):
        convert(
            local_file_path=valid_local_file_path,
            local_save_directory=valid_local_save_directory,
        )

    # next assert FileNotFoundError when attempting to read new file
    file_name = valid_local_file_path.split("/")[-1].split(".")[0]
    converted_file_path = valid_local_save_directory + "/" + file_name + ".mp3"

    with pytest.raises((FileNotFoundError, ValueError)):
        is_valid(local_file_path=converted_file_path)
