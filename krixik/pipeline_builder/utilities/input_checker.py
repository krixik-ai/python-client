import os
from krixik.pipeline_builder.utilities.chain_checker import chain_check
from krixik.utilities.validators.data.utilities.read_config import check_inverse_config
from krixik.modules.utilities.io_validator import is_valid


def input_check(local_file_path: str, module_chain: list) -> None:
    if not os.path.exists(local_file_path):
        raise FileExistsError(f"FAILURE: local_file_path does not exist - {local_file_path}")
    chain_check(module_chain)

    first_module = module_chain[0]
    first_module_input_format = first_module.input_format
    file_ext = "." + local_file_path.split(".")[-1]
    file_ext_format = check_inverse_config(file_ext)
    if file_ext_format != first_module_input_format:
        raise TypeError(f"file extension {file_ext} does not match the expected input format {first_module_input_format}")
    is_valid(first_module.name, local_file_path)
