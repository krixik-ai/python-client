from krixik.utilities.converters.docx_to_txt import (
    convert,
)
from tests.krixik import text_files_path
import pytest
import os

test_failure_data = [
    (None, None),
]


@pytest.mark.parametrize("local_file_path, local_save_directory", test_failure_data)
def test_failure(local_file_path, local_save_directory):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)):
        convert(
            local_file_path=local_file_path, local_save_directory=local_save_directory
        )


valid_local_file_path = text_files_path + "demo.docx"
valid_local_save_directory = text_files_path + "test_preprocessed"
if not os.path.exists(valid_local_save_directory):
    os.makedirs(valid_local_save_directory)

test_success_data = [
    (
        valid_local_file_path,
        valid_local_save_directory,
    ),  # local_save_directory provided
]


@pytest.mark.parametrize("local_file_path, local_save_directory", test_success_data)
def test_success(local_file_path, local_save_directory):
    assert (
        convert(
            local_file_path=local_file_path, local_save_directory=local_save_directory
        )
        is not None
    )


test_delete_data = [text_files_path + "Pride and Eights.docx"]


@pytest.mark.parametrize("local_file_path", test_delete_data)
def test_delete_on_failure(local_file_path):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)):
        convert(
            local_file_path=local_file_path,
            local_save_directory=valid_local_save_directory,
        )

    # next assert FileNotFoundError when attempting to read new file
    file_name = local_file_path.split("/")[-1].split(".")[0]
    converted_file_path = valid_local_save_directory + "/" + file_name + ".txt"
    with pytest.raises(FileNotFoundError):
        file = open(converted_file_path, "r")
        content = file.read(20)
