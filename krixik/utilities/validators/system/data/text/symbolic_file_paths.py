from krixik.utilities.validators.system.base.symbolic_paths import (
    symbolic_file_paths_checker as symbolic_file_paths_checker_utility,
)
from krixik.utilities.validators.system.base.symbolic_paths import (
    individual_symbolic_file_path_checker as individual_symbolic_file_path_checker_utility,
)
from krixik.utilities.validators.system.data.text import valid_extensions


def individual_symbolic_file_path_checker(file_path: str) -> None:
    return individual_symbolic_file_path_checker_utility(file_path, valid_extensions=valid_extensions)


def symbolic_file_paths_checker(symbolic_file_paths: list, verbose: bool = True) -> None:
    return symbolic_file_paths_checker_utility(symbolic_file_paths, valid_extensions=valid_extensions, verbose=verbose)
