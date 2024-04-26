from krixik.utilities.validators.system.base.local_file_path import (
    local_file_path_checker as local_file_path_checker_utility,
)
from krixik.utilities.validators.system.data.audio import valid_extensions


def local_file_path_checker(local_file_path: str) -> None:
    local_file_path_checker_utility(local_file_path)

    if "." + local_file_path.split(".")[-1] not in valid_extensions:
        raise ValueError(
            f"invalid local_file_path: please check that it ends with an allowed extension which include:  {valid_extensions} - your input local_file_path is: {local_file_path}"
        )
