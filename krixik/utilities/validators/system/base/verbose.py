def verbose_checker(verbose: bool | None = None) -> None:
    if verbose is None:
        raise TypeError("verbose must be a boolean")
    if not isinstance(verbose, bool):
        raise TypeError("verbose must be a boolean")
