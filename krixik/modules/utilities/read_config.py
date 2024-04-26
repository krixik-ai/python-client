import yaml
from krixik.__base__ import library_base_dir
from krixik.modules import available_modules


def get_module_config_by_name(module_name: str) -> dict:
    if module_name not in available_modules:
        raise ValueError(f"module {module_name} not found")
    config_path = f"{library_base_dir}/modules/{module_name}/module.yml"
    return get_module_available_defaults(config_path)


def get_module_available_defaults(config_path: str) -> dict:
    with open(config_path, "r") as file:
        # Load the YAML data from the file
        module_config = yaml.safe_load(file)["module"]

    module_name = module_config["name"]
    available_models = [v["name"] for v in module_config["models"]]
    default_model = module_config["defaults"]["model"]
    input_type = module_config["input"]
    output_type = module_config["output"]
    default_params = {}
    if "params" in module_config["defaults"]:
        default_params = module_config["defaults"]["params"]

    module_config_local = {
        "module_name": module_name,
        "available_models": available_models,
        "default_model": default_model,
        "default_params": default_params,
        "input_type": input_type,
        "output_type": output_type,
    }

    return module_config_local
