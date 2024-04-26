import yaml
from krixik.__base__ import library_base_dir

config_path = f"{library_base_dir}/utilities/converters/utilities/config.yml"


def convert_extension(extension: str) -> dict | None:
    with open(config_path, "r") as file:
        data_config = yaml.safe_load(file)["convertable_extensions"]
    simple_data_config = {k["name"]: k["convert"] for k in data_config}
    if extension not in list(simple_data_config.keys()):
        return None
    return simple_data_config[extension]
