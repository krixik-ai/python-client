from typing import Callable


def model_validator(model: dict, available_models: list) -> None:
    if not isinstance(model, str):
        raise ValueError(f"model: must be a string - the model entered is not in this required form - {model}")

    if model not in available_models:
        raise ValueError(f"model: must be one of {available_models} - the model entered is not in this required form - {model}")


def model_standardizer(model_selection: dict, default_model: str, default_params: dict) -> dict:
    if not isinstance(model_selection, dict):
        raise TypeError(
            f"model_selection: must be a dictionary with unique key(s): model, params - the model_selection entered is not in this required form - {model_selection}"
        )
    keys = list(model_selection.keys())
    if len(keys) > 2:
        raise ValueError(
            f"model_selection: must have only two keys: model, params - the model_selection entered is not in this required form - {model_selection}"
        )
    if len(set(keys) - set(["model", "params"])) > 0:
        raise ValueError(
            f"model_selection: must have only two keys: model, params - the model_selection entered is not in this required form - {model_selection}"
        )
    if "model" not in keys:
        model_selection["model"] = default_model
    if "params" not in keys:
        model_selection["params"] = default_params
    if len(model_selection["params"]) == 0:
        model_selection["params"] = default_params
    return model_selection


def model_selection_validator(model_selection: dict, available_models: list, params_validator: Callable) -> None:
    model = model_selection["model"]
    params = model_selection["params"]

    model_validator(model, available_models)

    params_validator(model, params)


def base_model_setup(
    model_selection: dict,
    available_models: list,
    default_model: str,
    default_params: dict,
    params_validator: Callable,
) -> dict:
    model_selection = model_standardizer(model_selection, default_model, default_params)

    model_selection_validator(model_selection, available_models, params_validator)

    return model_selection
