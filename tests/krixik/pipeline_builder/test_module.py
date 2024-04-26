from krixik.modules import available_modules
from krixik.pipeline_builder.module import Module
import pytest


test_failure_data = [
    1,
    [],
    "not-a-module",
]


@pytest.mark.parametrize("module_name", test_failure_data)
def test_1(module_name):
    """failure test for Module class - invalid module name"""
    with pytest.raises((Exception, ValueError)):
        Module(module_name)


test_success_data = available_modules


@pytest.mark.parametrize("module_name", test_success_data)
def test_2(module_name):
    """success test for Module class - valid module name"""
    Module(module_name)
