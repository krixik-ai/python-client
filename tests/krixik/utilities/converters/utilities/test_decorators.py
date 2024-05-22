from krixik.utilities.converters.utilities.decorators import (
    datatype_converter_wrapper,
)
import pytest
from krixik.__base__ import library_base_dir
from pathlib import Path

core_path = Path(library_base_dir)
parent_path = core_path.parent.absolute()


class MyClass:
    @datatype_converter_wrapper
    def my_method(
        self,
        *,
        local_file_path: str | None = None,
        local_save_directory: str | None = None,
        og_local_file_path: str | None = None,
        verbose: bool = True,
    ):
        return local_file_path, local_save_directory


success_test_data = [
    (f"{parent_path}/tests/test_files/text/1984_short.txt", True),
    (f"{parent_path}/tests/test_files/text/demo.docx", False),
    (f"{parent_path}/tests/test_files/images/family.png", True),
    (f"{parent_path}/tests/test_files/text/sample_article.txt", True),
    (f"{parent_path}/tests/test_files/text/chapter_1_short.pdf", False),
]


@pytest.mark.parametrize("local_file_path, expected", success_test_data)
def test_1(local_file_path, expected):
    """
    test successful data conversion / ignore for un-needed files
    """
    my_instance = MyClass()
    result_local_file_path, local_save_directory = my_instance.my_method(
        local_file_path=local_file_path
    )
    before_after_equal = True
    if result_local_file_path != local_file_path:
        before_after_equal = False
    assert before_after_equal is expected
