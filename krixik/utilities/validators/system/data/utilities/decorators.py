import yaml
import importlib
import inspect
from functools import wraps
from krixik.utilities.validators.system.base.verbose import verbose_checker
from krixik.utilities.validators.system.base.symbolic_paths import (
    individual_symbolic_directory_path_checker,
)
from krixik.__base__ import library_base_dir
from krixik.utilities.file_name_generator import generate_random_file_name
from krixik.utilities.utilities import vprint
from krixik.utilities.utilities import get_input
from krixik.utilities.validators.data.utilities.read_config import get_allowable_data_types
from krixik.modules.utilities.read_config import get_module_available_defaults
from krixik.utilities.validators.data.utilities.read_config import get_all_allowable_extensions
from krixik.utilities.validators.system.base.extension_enforcer import (
    pairwise_extension_checker,
)
from krixik.utilities.validators.system.base.symbolic_path_splitter import symbolic_path_splitter


def get_module_input_type(module_name: str) -> str:
    module_config_path = library_base_dir + f"/modules/{module_name}/module.yml"
    with open(module_config_path, "r") as file:
        module_config = yaml.safe_load(file)
        return module_config["module"]["input"]["type"]


def type_check_inputs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            signature = inspect.signature(func)
            self_arg = args[0] if args and hasattr(args[0], "__dict__") else None

            if "local_file_path" in list(kwargs.keys()):
                local_file_path = kwargs["local_file_path"]
                allowable_extensions = get_all_allowable_extensions()
                if "." + local_file_path.split(".")[-1] not in allowable_extensions:
                    raise ValueError(
                        f"the file extension '{local_file_path.split('.')[-1]}' is not allowed - current allowable extensions are {allowable_extensions}"
                    )

            # retrieve first module of pipeline
            pipeline_ordered_modules = self_arg.module_chain if self_arg else kwargs["pipeline_ordered_modules"]

            # load in appropriate module based on input type
            first_module = pipeline_ordered_modules[0]
            module_input_type = get_module_input_type(first_module)
            file_names_module = importlib.import_module(f"krixik.utilities.validators.system.data.{module_input_type}.file_names")
            local_file_path_module = importlib.import_module(f"krixik.utilities.validators.system.data.{module_input_type}.local_file_path")
            symbolic_file_paths_module = importlib.import_module(f"krixik.utilities.validators.system.data.{module_input_type}.symbolic_file_paths")

            file_names_checker = file_names_module.file_names_checker
            individual_file_name_checker = file_names_module.individual_file_name_checker
            local_file_path_checker = local_file_path_module.local_file_path_checker

            symbolic_file_paths_checker = symbolic_file_paths_module.symbolic_file_paths_checker
            individual_symbolic_file_path_checker = symbolic_file_paths_module.individual_symbolic_file_path_checker

            verbose = get_input("verbose", signature, kwargs, default_value=True)
            verbose_checker(verbose)

            file_names = None
            file_name = None
            local_file_path = None
            symbolic_file_paths = None
            symbolic_file_path = None
            symbolic_directory_path = None

            if "file_names" in list(kwargs.keys()):
                file_names = kwargs["file_names"]
                file_names_checker(file_names)

            if "file_name" in list(kwargs.keys()):
                file_name = kwargs["file_name"]
                individual_file_name_checker(file_name)

            if "local_file_path" in list(kwargs.keys()):
                local_file_path = kwargs["local_file_path"]
                local_file_path_checker(local_file_path)

                path_to_first_module = f"{library_base_dir}/modules/{first_module}/module.yml"
                default_module_config = get_module_available_defaults(path_to_first_module)
                input_type = default_module_config["input_type"]["type"]
                allowable_data_types = get_allowable_data_types(input_type)
                if "." + local_file_path.split(".")[-1] not in allowable_data_types:
                    raise ValueError(f"the file extension '{local_file_path.split('.')[-1]}' is not allowed for this module")

            if "symbolic_file_paths" in list(kwargs.keys()):
                symbolic_file_paths = kwargs["symbolic_file_paths"]
                symbolic_file_paths_checker(symbolic_file_paths)

            if "symbolic_file_path" in list(kwargs.keys()):
                symbolic_file_path = kwargs["symbolic_file_path"]
                individual_symbolic_file_path_checker(symbolic_file_path)

            if "symbolic_directory_path" in list(kwargs.keys()):
                symbolic_directory_path = kwargs["symbolic_directory_path"]
                individual_symbolic_directory_path_checker(symbolic_directory_path)

            if (file_name is not None or symbolic_directory_path is not None) and symbolic_file_path is not None:
                raise ValueError("file_name and symbolic_directory_path cannot both be given if symbolic_file_path is given")

            if symbolic_file_path is not None:
                symbolic_directory_path, file_name = symbolic_path_splitter(symbolic_file_path)
                kwargs["symbolic_file_path"] = None
                kwargs["symbolic_directory_path"] = symbolic_directory_path
                kwargs["file_name"] = file_name

            if "file_name" in list(kwargs.keys()) and "local_file_path" in list(kwargs.keys()):
                if "og_local_file_path" in list(kwargs.keys()):
                    local_file_path = kwargs["og_local_file_path"]

                if file_name is not None and local_file_path is not None:
                    pairwise_extension_checker(file_name, local_file_path)

                if file_name is None and local_file_path is not None:
                    file_name = generate_random_file_name(local_file_path.split(".")[-1])
                    kwargs["file_name"] = file_name
                    vprint(
                        f"INFO: file_name was not set by user - setting to random file name: {file_name}",
                        verbose=verbose,
                    )

        except ValueError as e:
            raise ValueError(e)
        except TypeError as e:
            raise TypeError(e)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except PermissionError as e:
            raise PermissionError(e)
        except Exception as e:
            raise Exception(e)

        return func(self_arg, *args[1:], **kwargs)

    setattr(wrapper, "system_data_type_checked", bool(True))
    return wrapper
