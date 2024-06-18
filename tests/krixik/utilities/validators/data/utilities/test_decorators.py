from krixik.utilities.validators.system.data.utilities.decorators import (
    type_check_inputs as data_type_check_inputs,
)
import pytest
from krixik.__base__ import library_base_dir
from pathlib import Path
from typing import Optional

core_path = Path(library_base_dir)
parent_path = core_path.parent.absolute()


class MySystemDataClass:
    def __init__(self, pipeline_ordered_modules):
        self.module_chain = pipeline_ordered_modules

    @data_type_check_inputs
    def my_method(
        self,
        *,
        file_name: Optional[str] = None,
        local_file_path: Optional[str] = None,
        modules: dict,
        symbolic_directory_path: Optional[str] = None,
        file_tags: Optional[list] = None,
        expire_time: Optional[int] = None,
    ):
        return True


file_name = "tesFFt.txt"
symbolic_directory_path = "/home/UsEr"
local_file_path = f"{parent_path}/tests/test_files/text/1984_short.txt"
pipeline_ordered_modules = ["parser", "text-embedder"]
modules = {}
expire_time = 60*30
file_tags = [{"valid": "tag"}]


def test_1():
    """
    loose success tests to ensure system data decorator is wrappipng system data validators correctly.
    each system data validator itself is tested more thoroughly in its own test file.
    """
    instance = MySystemDataClass(pipeline_ordered_modules=pipeline_ordered_modules)
    assert instance.my_method(
        file_name=file_name,
        local_file_path=local_file_path,
        modules=modules,
        symbolic_directory_path=symbolic_directory_path,
        file_tags=file_tags,
        expire_time=expire_time,
    )


def test_2(subtests):
    """
    loose failure tests to ensure system data decorator is wrappipng system data validators correctly.
    each system data validator itself is tested more thoroughly in its own test file.
    """
    with subtests.test(msg="invalid file name test"):
        with pytest.raises(ValueError, match=r".*invalid file_name\.*"):
            instance = MySystemDataClass(
                pipeline_ordered_modules=pipeline_ordered_modules
            )
            instance.my_method(
                file_name="tesFFt.mp3",
                local_file_path=local_file_path,
                modules=modules,
                symbolic_directory_path=symbolic_directory_path,
                file_tags=file_tags,
                expire_time=expire_time,
            )

    with subtests.test(msg="file_name local_file_path mismatch test"):
        with pytest.raises(
            ValueError,
            match=r".*input file_name extension must match input local_file_path extension\.*",
        ):
            instance = MySystemDataClass(
                pipeline_ordered_modules=pipeline_ordered_modules
            )
            instance.my_method(
                file_name="tesFFt.docx",
                local_file_path=local_file_path,
                modules=modules,
                symbolic_directory_path=symbolic_directory_path,
                file_tags=file_tags,
                expire_time=expire_time,
            )
