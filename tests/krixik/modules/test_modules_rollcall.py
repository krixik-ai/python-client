import os
from krixik.modules import available_modules
from tests import test_base_dir

modules_directory = test_base_dir + "/krixik/modules"
not_modules = ["__pycache__", "utilities"]
test_dir_available_modules = [
    name
    for name in os.listdir(modules_directory)
    if os.path.isdir(os.path.join(modules_directory, name)) and name not in not_modules
]
test_dir_available_modules.sort()


def test_available_modules():
    """ensure that modules directories in krixik and test are the same"""
    assert available_modules == test_dir_available_modules
