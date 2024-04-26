from krixik.modules.utilities.io_validator import is_valid
from tests.krixik import text_files_path, json_files_path, image_files_path
import pytest

test_success_data = [
     ("summarize", f"{text_files_path}/1984_short.txt"),
 ]

@pytest.mark.parametrize("module_name, file_path", test_success_data)
def test_is_valid_success(module_name, file_path):
    is_valid(module_name, file_path)

