from krixik.utilities.validators.system.base.utilities.decorators import (
    type_check_inputs as base_type_check_inputs,
)
from krixik.__base__ import library_base_dir
from pathlib import Path

core_path = Path(library_base_dir)
parent_path = core_path.parent.absolute()


class MySystemBaseClass:
    @base_type_check_inputs
    def my_method(
        self,
        *,
        file_name: str | None = None,
        local_file_path: str | None = None,
        symbolic_directory_path: str | None = None,
        file_tags: list | None = None,
        expire_time: int | None = None,
    ):
        return True


file_name = "tesFFt.txt"
symbolic_directory_path = "/home/UsEr"
local_file_path = f"{parent_path}/tests/test_files/text/1984_short.txt"
pipeline_ordered_modules = ["parser", "text-embedder"]
modules = {}
expire_time = 900
file_tags = [{"valid": "tag"}]


def test_1():
    """
    loose tests to ensure base decorator is wrappipng base validators correctly.
    each base validator itself is tested more thoroughly in its own test file.
    """
    instance = MySystemBaseClass()
    assert instance.my_method(
        file_name=file_name,
        local_file_path=local_file_path,
        symbolic_directory_path=symbolic_directory_path,
        file_tags=file_tags,
        expire_time=expire_time,
    )
