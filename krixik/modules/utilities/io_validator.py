import json
import copy
import importlib
from krixik.utilities.validators.data import available_data_types


def format_checker(format_: str, local_file_path: str) -> None:
    if format_ not in available_data_types:
        raise ValueError("FAILURE: format not supported")

    if format_ == "json":
        try:
            with open(local_file_path, "r") as file:
                data = json.load(file)
                first_dict = data[0]
        except Exception as e:
            raise ValueError(f"FAILURE: loading json file: {e}")


def process_key_checker(required_structure: dict, file_path: str) -> None:
    if "process_key" not in required_structure.keys():
        raise ValueError(f"FAILURE: process_key not found in required_structure")
    with open(file_path, "r") as file:
        data = json.load(file)
    data_copy = copy.deepcopy(data)
    if isinstance(data, list):
        data_copy = data_copy[0]
    else:
        raise ValueError("FAILURE: input data must be a list of dictionaries")
    if not isinstance(data_copy, dict):
        raise ValueError("FAILURE: input data must be a list of dictionaries")
    process_key = required_structure["process_key"]
    if process_key not in data_copy.keys():
        raise ValueError(f"FAILURE: required process_key {process_key} not found in data")


def validate_json_file_structure(required_structure: dict, file_path: str) -> None:
    try:
        # test that format is correct
        format_checker(required_structure["format"], file_path)

        # check that input file_path contains process_key
        if required_structure["format"] == "json":
            process_key_checker(required_structure, file_path)

    except Exception as e:
        raise e


def is_valid(module_name: str, file_path: str) -> None:
    try:
        module_io_path = f"krixik.modules.{module_name}.io"
        module = importlib.import_module(module_io_path)
        InputStructure = module.InputStructure
        input_structure = InputStructure().__dict__

        validate_json_file_structure(input_structure, file_path)
    except Exception as e:
        raise e
