import yaml
from krixik.modules.caption import module_config_path
from krixik.modules.utilities.read_config import (
    get_module_available_defaults,
)


def test_module_config():
    """confirm that default module config provided in module init is the same as the module (subset) config provided in the module.yml file"""
    with open(module_config_path, "r") as file:
        module_config = yaml.safe_load(file)["module"]
    module_name = module_config["name"]
    available_models = [v["name"] for v in module_config["models"]]
    default_model = module_config["defaults"]["model"]
    input_type = module_config["input"]
    output_type = module_config["output"]
    default_params = {}
    if "params" in module_config["defaults"]:
        default_params = module_config["defaults"]["params"]

    module_config_subset = {
        "module_name": module_name,
        "available_models": available_models,
        "default_model": default_model,
        "default_params": default_params,
        "input_type": input_type,
        "output_type": output_type,
    }

    default_config = get_module_available_defaults(
        module_config_path
    )
    assert module_config_subset == default_config
