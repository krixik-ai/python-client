import yaml
import os


def config_check(filename):
    if not os.path.exists(filename):
        raise FileExistsError(f"FAILURE: config file does not exist - {filename}")
    
            
    file_size_bytes = os.path.getsize(filename)
    file_size_mb = file_size_bytes / (1024 * 1024)
    max_config_size=1
    if file_size_mb >= max_config_size:
        raise ValueError(f"FAILURE: the size of your input configuration file is greater than {max_config_size}MB - the maximum size allowed - please check this file to ensure it only contains your pipeline configuration: {filename}")

    _, extension = os.path.splitext(filename)
    if extension.lower() == ".yaml" or extension.lower() == ".yml":
        try:
            with open(filename, "r") as file:
                yaml.safe_load(file)
        except yaml.YAMLError:
            raise yaml.YAMLError(f"FAILURE: config is not a valid yaml - {filename}")
    else:
        raise ValueError(f"FAILURE: config - {filename} - does not end with valid extension .yml or .yaml")
