def use_default_clean_options_checker(use_default_clean_options: bool) -> None:
    # check that use_default_clean_options is not None
    if use_default_clean_options is not None:
        # check that use_default_clean_options is a bool
        if not isinstance(use_default_clean_options, bool):
            raise TypeError("use_default_clean_options is not a bool")
