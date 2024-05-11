import os


def local_file_path_checker(local_file_path: str) -> None:
    if local_file_path is None:
        raise ValueError("local_file_path cannot be empty")

    if isinstance(local_file_path, str) is False:
        raise TypeError(f"invalid local file path: not a string - {local_file_path}")

    if os.path.exists(local_file_path) is False:
        raise FileNotFoundError(f"invalid local file path: does not exist - {local_file_path}")
