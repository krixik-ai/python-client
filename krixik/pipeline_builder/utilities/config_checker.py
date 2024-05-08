import yaml
import os


def config_check(filename):
    if not os.path.exists(filename):
        raise FileExistsError(f"FAILURE: config file does not exist - {filename}")

    _, extension = os.path.splitext(filename)
    if extension.lower() == ".yaml" or extension.lower() == ".yml":
        try:
            with open(filename, "r") as file:
                yaml.safe_load(file)
        except yaml.YAMLError:
            raise yaml.YAMLError(f"FAILURE: config is not a valid yaml - {filename}")
    else:
        raise ValueError(f"FAILURE: config - {filename} - does not end with valid extension .yml or .yaml")
