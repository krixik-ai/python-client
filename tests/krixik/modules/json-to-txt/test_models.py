import importlib
from pyexpat import model
import pytest
module = importlib.import_module("krixik.modules.json-to-txt")
module_config = module.module_config
models = importlib.import_module("krixik.modules.json-to-txt.models")
model_selection_setup = models.model_selection_setup
test_data = importlib.import_module("tests.krixik.modules")
baseline_test_failue_data = test_data.baseline_failure_model_data
available_models = module_config["available_models"]
default_model = module_config["default_model"]
default_params = module_config["default_params"]


failure_test_data = baseline_test_failue_data + [
    {
        "mdoel": "not a model at all"
    },
]


@pytest.mark.parametrize("test_data", failure_test_data)
def test_1(test_data):
    with pytest.raises((ValueError, TypeError)):
        model_selection_setup(test_data)


test_success_data = [{"model": a} for a in available_models]

default_selected_model = {"model": default_model, "params": default_params}


@pytest.mark.parametrize("test_data", test_success_data)
def test_2(test_data):
    instance = model_selection_setup(test_data)
    assert instance.get_setup_result() == test_data
