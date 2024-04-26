from krixik.modules.utilities.io_validator import is_valid
from tests.krixik import image_files_path
import pytest


test_success_data = [
     ("ocr", f"{image_files_path}/resturant.png"),
     ("ocr", f"{image_files_path}/big2.jpeg"),
     ("ocr", f"{image_files_path}/big.jpg"),
 ]

@pytest.mark.parametrize("module_name, file_path", test_success_data)
def test_is_valid_success(module_name, file_path):
    is_valid(module_name, file_path)

