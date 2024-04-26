from krixik.modules.utilities.io_validator import is_valid
from tests.krixik import audio_files_path
import pytest


test_success_data = [
     ("transcribe", f"{audio_files_path}/Is AI Actually Useful short.mp3"),
 ]

@pytest.mark.parametrize("module_name, file_path", test_success_data)
def test_is_valid_success(module_name, file_path):
    is_valid(module_name, file_path)
