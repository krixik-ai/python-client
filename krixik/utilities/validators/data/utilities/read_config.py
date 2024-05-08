import yaml
from krixik.__base__ import library_base_dir

config_path = f"{library_base_dir}/utilities/validators/data/utilities/config.yml"


def get_config() -> dict:
    with open(config_path, "r") as file:
        data_config = yaml.safe_load(file)["data_types"]

    return data_config


def get_inverse_config() -> dict:
    with open(config_path, "r") as file:
        data_config = yaml.safe_load(file)["data_types"]

    inverse_data_config = {}
    for data_type, extensions in data_config.items():
        for extension in extensions:
            inverse_data_config[extension] = data_type

    return inverse_data_config


def check_inverse_config(ext: str) -> dict:
    with open(config_path, "r") as file:
        data_config = yaml.safe_load(file)["data_types"]
    available_data_types = list(data_config.keys())

    inverse_data_config = {}
    for data_type, extensions in data_config.items():
        for extension in extensions:
            inverse_data_config[extension] = data_type
    try:
        return inverse_data_config[ext]
    except KeyError:
        raise ValueError(f"extension '{ext}' does not map to any currently available data types: {available_data_types} ")


def get_allowable_data_types(data_type: str) -> dict:
    with open(config_path, "r") as file:
        data_config = yaml.safe_load(file)["data_types"]

    if data_type not in data_config:
        raise ValueError(f"data_type: must be one of {data_config} - the data_type entered is not in this required form - {data_type}")
    return data_config[data_type]


def get_all_allowable_extensions() -> list:
    with open(config_path, "r") as file:
        data_config = yaml.safe_load(file)["data_types"]
    all_extension_lists = [v for k, v in data_config.items()]
    all_extensions = []
    for extension_list in all_extension_lists:
        all_extensions += extension_list
    return all_extensions
