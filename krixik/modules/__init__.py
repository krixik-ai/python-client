import os
import importlib
import yaml
from krixik.__base__ import library_base_dir

modules_directory = library_base_dir + "/modules"
not_modules = ["__pycache__", "utilities"]
available_modules = [
    name for name in os.listdir(modules_directory) if os.path.isdir(os.path.join(modules_directory, name)) and name not in not_modules
]
available_modules.sort()


def get_module_details(module_name: str) -> dict:
    if not isinstance(module_name, str):
        raise Exception(f"module_name must be a string, your input {module_name} is of type {type(module_name)}")

    if module_name not in available_modules:
        raise Exception(f"user defined module {module_name} does not exist, currently available modules: {available_modules}")

    module_config_path = library_base_dir + f"/modules/{module_name}/module.yml"
    io_module_path = f"krixik.modules.{module_name}.io"

    module_config = None
    input_data_example = None
    output_data_example = None

    with open(module_config_path, "r") as file:
        module_config = yaml.safe_load(file)

    io_module = importlib.import_module(io_module_path)

    input_data_structure = io_module.InputStructure if hasattr(io_module, "InputStructure") else None
    if input_data_structure is not None:
        input_data_example = input_data_structure().data_example if hasattr(input_data_structure, "data_example") else None

    output_data_structure = io_module.OutputStructure if hasattr(io_module, "OutputStructure") else None

    if output_data_structure is not None:
        output_data_example = output_data_structure().data_example if hasattr(output_data_structure, "data_example") else None

    module_package = {
        "module_config": module_config,
        "input_data_example": input_data_example,
        "output_data_example": output_data_example,
    }

    return module_package
