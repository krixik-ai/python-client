def wait_for_process_checker(wait_for_process: bool | None = None) -> None:
    if wait_for_process is None:
        raise TypeError("wait_for_process must be a boolean")
    if not isinstance(wait_for_process, bool):
        raise TypeError("wait_for_process must be a boolean")
