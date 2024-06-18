from krixik.utilities.validators.data.utilities.decorators import (
    datatype_validator,
)
import pytest
from krixik.__base__ import library_base_dir
from pathlib import Path
from typing import Optional

core_path = Path(library_base_dir)
parent_path = core_path.parent.absolute()


success_test_data = [
    f"{parent_path}/tests/test_files/text/1984_short.txt",
    f"{parent_path}/tests/test_files/text/demo.docx",
    f"{parent_path}/tests/test_files/images/family.png",
    f"{parent_path}/tests/test_files/text/sample_article.txt",
    f"{parent_path}/tests/test_files/json/valid_1.json",
]


class MyClass:
    @datatype_validator
    def my_method(
        self,
        *,
        local_file_path: Optional[str] = None,
    ):
        return True


@pytest.mark.parametrize("local_file_path", success_test_data)
def test_success(local_file_path):
    my_instance = MyClass()
    assert my_instance.my_method(local_file_path=local_file_path) is True


test_failure_data = ["not_an_extension.abcdefg", "not_valid_yet.zip"]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_failure(local_file_path):
    with pytest.raises(ValueError, match=r".*invalid file extension\.*"):
        my_instance = MyClass()
        my_instance.my_method(local_file_path=local_file_path)
