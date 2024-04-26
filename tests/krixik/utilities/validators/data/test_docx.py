from krixik.utilities.validators.data.docx import is_valid
from krixik.utilities.validators.data.docx import is_size
from tests.krixik import text_files_path
import pytest

# first - check is_valid
test_failure_data = [
    text_files_path + "chapter_1_short.txt",
    text_files_path + "chapter_1_short.pdf",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_1(local_file_path):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)) as excinfo:
        is_valid(local_file_path=local_file_path)


test_success_data = [text_files_path + "demo.docx"]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_2(local_file_path):
    assert is_valid(local_file_path=local_file_path) is None


# second - check is_size
test_data_failure = [
    text_files_path + "Empty McFile.pdf",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_3(local_file_path):
    with pytest.raises((ValueError, TypeError, FileNotFoundError)) as excinfo:
        is_size(
            local_file_path=local_file_path,
            minimum_word_count=10,
            minimum_file_size=0.000001,
            maximum_file_size=100.0,
        )


test_data_success = [text_files_path + "demo.docx"]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_4(local_file_path):
    assert (
        is_size(
            local_file_path=local_file_path,
            minimum_word_count=10,
            minimum_file_size=0.000001,
            maximum_file_size=100.0,
        )
        is None
    )
