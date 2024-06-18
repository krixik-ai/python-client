from typing import Optional


def verbose_checker(verbose: Optional[bool] = None) -> None:
    if verbose is None:
        raise TypeError("verbose must be a boolean")
    if not isinstance(verbose, bool):
        raise TypeError("verbose must be a boolean")
