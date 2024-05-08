from krixik.modules.transcribe import module_config
from krixik.modules.utilities.model import base_model_setup
from krixik.modules.utilities.model_selection import ModelSelection

available_models = module_config["available_models"]
default_model = module_config["default_model"]
default_params = module_config["default_params"]


def params_validator(model: str, params: dict) -> None:
    if len(params) != 0:
        raise ValueError(f"params must have no values - the params entered is not in this required form - {params}")


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
