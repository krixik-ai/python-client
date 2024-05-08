def name_check(name: str) -> None:
    if not isinstance(name, str):
        raise ValueError(f"FAILURE: your custom pipeline name - {name} - is not a string")
    if len(name) == 0 or len(name) > 64:
        raise ValueError(f"FAILURE: your name - {name} - must be greater than 1 and less than 64 characters")
