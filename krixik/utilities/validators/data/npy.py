import os
import numpy as np


def is_valid(local_file_path: str) -> None:
    try:
        # check that local_file_path is a text file
        _, file_extension = os.path.splitext(local_file_path)
        if file_extension not in [".npy"]:
            raise ValueError(f"invalid local_file_path: please check that it is an npy file - {local_file_path}")
        np_array = np.load(local_file_path, mmap_mode="r")
        partial_array = np_array[:4096]
    except UnicodeDecodeError:
        raise ValueError(f"invalid local_file_path: please check that it is an npy file - {local_file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"the file '{local_file_path}' does not exist.")
    except Exception as e:
        raise ValueError(f"npy validation failed with exception {e}")


def is_size(
    *,
    local_file_path: str | None,
    minimum_word_count: int = 6,
    maximum_line_count: int = 100000,
    minimum_file_size: float = 0.000001,
    maximum_file_size: float = 3.000001,
) -> None:
    # proper size
    def compute_size(file_path: str):
        try:
            # Get the size of the file in bytes
            file_size_bytes = os.path.getsize(file_path)

            # Convert the size to megabytes (MB)
            file_size_mb = file_size_bytes / (1024 * 1024)
            return file_size_mb
        except Exception as e:
            raise ValueError(f"text size calculation failed with exception {e}")

    # check size of input text file
    if local_file_path is None:
        raise ValueError("invalid local_file_path - local_file_path cannot be None")
    try:
        # check that local_file_path represents a valid text file
        is_valid(local_file_path)

        # compute file size in megabytes
        file_size = compute_size(local_file_path)

        # check that file size in megabytes is greater than minimum_file_size and less than maximum_file_size
        if file_size < minimum_file_size:
            raise ValueError(
                f"input file size is {file_size} megabytes: either less than {minimum_file_size} megabytes (current minimum size allowable) or greater than {maximum_file_size} megabytes (current maximum size allowable) - {local_file_path}"
            )
        if file_size > maximum_file_size:
            raise ValueError(f"file size is greater than {maximum_file_size} megabytes (current maximum size allowable) - {local_file_path}")

    except ValueError as ve:
        raise ve

    except Exception as e:
        raise ValueError(f"text extraction failed with exception {e}")
