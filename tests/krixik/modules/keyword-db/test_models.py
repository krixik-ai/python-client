import importlib
import pytest

module = importlib.import_module("krixik.modules.keyword-db")
module_config = module.module_config
module_selector = importlib.import_module("krixik.modules.keyword-db.models")
model_selection_setup = module_selector.model_selection_setup
test_data = importlib.import_module("tests.krixik.modules")
baseline_test_failue_data = test_data.baseline_failure_model_data
available_models = module_config["available_models"]
default_model = module_config["default_model"]
default_params = module_config["default_params"]


failure_test_data = baseline_test_failue_data + []


@pytest.mark.parametrize("test_data", failure_test_data)
def test_model_selection_setup_failure(test_data):
    with pytest.raises(ValueError):
        model_selection_setup(test_data)


test_success_data = [{"model": a} for a in available_models]

default_selected_model = {"model": default_model, "params": default_params}


@pytest.mark.parametrize("test_data", test_success_data)
def test_model_selection_setup_success(test_data):
    instance = model_selection_setup(test_data)
    assert instance.get_setup_result() == test_data
