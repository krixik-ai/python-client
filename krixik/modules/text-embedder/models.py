import importlib
from krixik.modules.utilities.model import base_model_setup
from krixik.modules.utilities.model_selection import ModelSelection

module = importlib.import_module("krixik.modules.text-embedder")
module_config = module.module_config
available_models = module_config["available_models"]
default_model = module_config["default_model"]
default_params = module_config["default_params"]
module = importlib.import_module("krixik.modules.text-embedder.params")
quantize_validator = module.quantize_validator


def params_validator(model: str, params: dict) -> None:
    if len(params) != 1:
        raise ValueError(f"params: must have only one key-value pair - the params entered are not in this required form - {params}")
    quantize_validator(params)


def model_setup(model_selection: dict):
    return base_model_setup(
        model_selection,
        available_models,
        default_model,
        default_params,
        params_validator,
    )


def model_selection_setup(data: dict) -> ModelSelection:
    return ModelSelection(data, model_setup)
