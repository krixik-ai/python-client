import os


def local_save_directory_checker(local_save_directory: str) -> None:
    if local_save_directory is not None:
        if not isinstance(local_save_directory, str):
            raise TypeError(f"invalid local save directory: not a string - {local_save_directory}")

        if os.path.isdir(local_save_directory) is False:
            raise FileNotFoundError(f"invalid local save directory: does not exist - {local_save_directory}")

        if os.access(local_save_directory, os.W_OK) is False:
            raise PermissionError(f"invalid local save directory: write access denied - {local_save_directory}")

        if os.access(local_save_directory, os.R_OK) is False:
            raise PermissionError(f"invalid local save directory: read access denied - {local_save_directory}")
