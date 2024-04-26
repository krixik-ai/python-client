from krixik.utilities.validators.system.base.extension_enforcer import (
    pairwise_extension_checker,
)
from tests.krixik import text_files_path
import pytest

test_data_failure = [
    ("my_life_and_work_full.txt", "chapter_1_short.pdf"),
    ("my_life_and_work_full.txt", "demo.docx"),
    ("my_life_and_work_full.doc", "demo.docx"),
    ("my_life_and_work_full.doc", "a sample slide.pptx"),
]

# with pytest.raises((ValueError, TypeError))


@pytest.mark.parametrize("file_name, local_file_path_name", test_data_failure)
def test_failure(file_name, local_file_path_name):
    with pytest.raises(ValueError):
        pairwise_extension_checker(file_name, text_files_path + local_file_path_name)


test_data_success = [
    ("my_life_and_work_full.pdf", "chapter_1_short.pdf"),
    ("my_life_and_work_full.docx", "demo.docx"),
    ("my_life_and_work_full.mp3", "Agenda - Oct 2023 Summit.mp3"),
    ("my_life_and_work_full.abc", "a sample slide.abc"),
]


@pytest.mark.parametrize("file_name, local_file_path_name", test_data_success)
def test_success(file_name, local_file_path_name):
    assert (
        pairwise_extension_checker(file_name, text_files_path + local_file_path_name)
        is None
    )
