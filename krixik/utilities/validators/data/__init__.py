from os import listdir
from os.path import isfile, join
from krixik.__base__ import library_base_dir

data_directory = library_base_dir + "/utilities/validators/data"
not_data = [
    "__pycache__",
    "utilities",
    "__init__.py",
    "read_config.py",
    "config.yml",
    "decorators.py",
]
available_data_types = [
    name.split(".")[0]
    for name in [f for f in listdir(data_directory) if isfile(join(data_directory, f))]
    if name not in not_data and len(name.split(".")[0]) > 0
]
