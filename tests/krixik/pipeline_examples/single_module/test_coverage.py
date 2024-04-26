from krixik.modules import available_modules
from tests.krixik.pipeline_examples.single_module.utilities.test_data import module_test_data
from tests import test_base_dir
import os


def test_1():
    """ Test that all available modules are accounted for in the test data """
    assert available_modules == list(module_test_data.keys())


def test_2():
    """make sure tests exist to cover all available single module pipelines"""
    single_modules_test_dir = test_base_dir + "/krixik/pipeline_examples/single_module/modules"
    not_modules = ["__pycache__", "utilities", "test_coverage.py", "test_generate_examples.py", "__init__.py", ".DS_Store"]
    available_module_tests = [
        name
        for name in os.listdir(single_modules_test_dir)
        if not os.path.isdir(os.path.join(single_modules_test_dir, name)) and name not in not_modules
    ]
    available_module_tests = [name.split("test_")[1].split(".py")[0] for name in available_module_tests]
    available_module_tests.sort()

    assert available_module_tests == available_modules
