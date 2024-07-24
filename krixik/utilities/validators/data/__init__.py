from os import listdir
from os.path import isfile, join
from math import floor, log10
from krixik.__base__ import library_base_dir

data_directory = library_base_dir + "/utilities/validators/data"
not_data = ["__pycache__", "utilities", "__init__.py", "read_config.py", "config.yml", "decorators.py", "video.py"]
available_data_types = [
    name.split(".")[0]
    for name in [f for f in listdir(data_directory) if isfile(join(data_directory, f))]
    if name not in not_data and len(name.split(".")[0]) > 0
]


def num_zeros_plus_one(decimal):
    return 1 if decimal == 0 else -floor(log10(abs(decimal))) + 1


def file_size_check(local_file_path: str, file_size: float, minimum_file_size: float, maximum_file_size: float) -> None:
    # check that file size in megabytes is greater than minimum_file_size and less than maximum_file_size
    if file_size < minimum_file_size:
        raise ValueError(
            f"input file size is {round(file_size, num_zeros_plus_one(minimum_file_size))} megabytes: less than {minimum_file_size} megabytes (current minimum size allowable)"
        )

    if file_size > maximum_file_size:
        raise ValueError(
            f"***Krixik Open Beta warning*** input file size is {round(file_size, num_zeros_plus_one(maximum_file_size))} megabytes: greater than {maximum_file_size} megabytes (current maximum size allowable) - {local_file_path}"
        )
