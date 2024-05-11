from krixik.utilities.validators.system.base.file_names import (
    file_names_checker as file_names_checker_utility,
)
from krixik.utilities.validators.system.base.file_names import (
    individual_file_name_checker as individual_file_name_checker_utility,
)
from krixik.utilities.validators.system.data.text import valid_extensions


def individual_file_name_checker(file_name: str, phase: str = "other") -> None:
    # use utility function
    individual_file_name_checker_utility(file_name, phase=phase, valid_extensions=valid_extensions)


def file_names_checker(file_names: list, phase: str = "other", verbose: bool = True) -> None:
    # use utility function
    file_names_checker_utility(file_names, phase=phase, valid_extensions=valid_extensions, verbose=verbose)
