from krixik.utilities.validators.system import MAX_FILES_COUNT


def max_files_checker(max_files: int) -> None:
    if max_files is not None:
        # check that max_files is an integer
        if not isinstance(max_files, int) or isinstance(max_files, bool):
            raise TypeError(f"invalid max_files: not an integer - {max_files}")

        if max_files < 1:
            raise ValueError(f"invalid max_files: less than 1 - {max_files}")

        if max_files > MAX_FILES_COUNT:
            raise ValueError(f"invalid max_files: greater than {MAX_FILES_COUNT} - {max_files}")

        if max_files < 1:
            raise ValueError(f"invalid max_files: less than 1 - {max_files}")
