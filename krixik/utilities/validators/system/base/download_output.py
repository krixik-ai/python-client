def download_output_checker(download_output: bool | None = None) -> None:
    if download_output is None:
        raise TypeError("download_output must be a boolean")
    if not isinstance(download_output, bool):
        raise TypeError("download_output must be a boolean")
