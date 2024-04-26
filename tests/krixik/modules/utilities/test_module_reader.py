import importlib
import pytest

from krixik.modules import available_modules

test_success_data = available_modules


@pytest.mark.parametrize("module", test_success_data)
def test_available_modules_success(module):
    base = importlib.import_module(f"krixik.modules.{module}")
    module_config = base.module_config
    assert True


test_failure_data = ["blah", "never-a-module", "what-were-you-thinking"]


@pytest.mark.parametrize("module", test_failure_data)
def test_available_modules_failure(module):
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(f"krixik.modules.{module}")
