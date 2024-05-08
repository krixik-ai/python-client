import os
import inspect
from functools import wraps

from krixik.utilities.validators.system.base.version import version_checker
from krixik.utilities.validators.system.base.file_ids import file_ids_checker
from krixik.utilities.validators.system.base.file_ids import individual_file_id_checker
from krixik.utilities.validators.system.base.file_tags import file_tags_checker
from krixik.utilities.validators.system.base.symbolic_paths import (
    symbolic_directory_paths_checker,
)
from krixik.utilities.validators.system.base.symbolic_paths import (
    individual_symbolic_directory_path_checker,
)
from krixik.utilities.validators.system.base.request_id import (
    request_id_checker,
)
from krixik.utilities.validators.system.base.verbose import verbose_checker
from krixik.utilities.validators.system.base.max_files import max_files_checker
from krixik.utilities.validators.system.base.file_description import (
    file_description_checker,
)
from krixik.utilities.validators.system.base.timestamp_bookends import (
    timestamp_bookends_checker,
)
from krixik.utilities.validators.system.base.local_save_directory import (
    local_save_directory_checker,
)
from krixik.utilities.validators.system.base.wait_for_process import (
    wait_for_process_checker,
)
from krixik.utilities.validators.system.base.sort_order import (
    sort_order_checker,
)
from krixik.utilities.validators.system.base.expire_time import expire_time_checker
from krixik.utilities.validators.system.base.query import query_checker
from krixik.utilities.validators.system.base.k_nn import k_checker
from krixik.utilities.validators.system.base.user_secrets import (
    api_key_checker,
    api_url_checker,
)

from krixik.utilities.utilities import get_input
from typing import Callable


def type_check_inputs(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func_name = func.__name__
            signature = inspect.signature(func)

            verbose = get_input("verbose", signature, kwargs, default_value=True)
            verbose_checker(verbose)

            if "api_key" in list(kwargs.keys()):
                api_key_checker(kwargs["api_key"])

            if "api_url" in list(kwargs.keys()):
                api_url_checker(kwargs["api_url"])

            if "expire_time" in list(kwargs.keys()):
                expire_time_checker(kwargs["expire_time"])

            if "version" in list(kwargs.keys()):
                version_checker(kwargs["version"])

            if "file_ids" in list(kwargs.keys()):
                file_ids_checker(kwargs["file_ids"])

            if "file_id" in list(kwargs.keys()):
                individual_file_id_checker(kwargs["file_id"])

            if "file_tags" in list(kwargs.keys()):
                file_tags_checker(kwargs["file_tags"])

            if "symbolic_directory_paths" in list(kwargs.keys()):
                symbolic_directory_paths_checker(kwargs["symbolic_directory_paths"])

            if "symbolic_directory_path" in list(kwargs.keys()):
                individual_symbolic_directory_path_checker(kwargs["symbolic_directory_path"])

            sort_order = get_input("sort_order", signature, kwargs, default_value="descending")
            if sort_order is not None:
                sort_order_checker(sort_order)

            if "process_id" in list(kwargs.keys()):
                request_id_checker(kwargs["process_id"])

            if "request_id" in list(kwargs.keys()):
                request_id_checker(kwargs["request_id"])

            if "local_save_directory" in list(kwargs.keys()):
                local_save_directory_checker(kwargs["local_save_directory"])

            if "file_description" in list(kwargs.keys()):
                file_description_checker(kwargs["file_description"])

            max_files = get_input("max_files", signature, kwargs)
            if max_files is not None:
                max_files_checker(max_files)

            wait_for_process = get_input("wait_for_process", signature, kwargs, default_value=False)
            wait_for_process_checker(wait_for_process)

            query = get_input("query", signature, kwargs)
            if query is not None:
                query_checker(query)

            k = get_input("k", signature, kwargs)
            if k is not None:
                k_checker(k)

            created_at_start = get_input("created_at_start", signature, kwargs)
            created_at_end = get_input("created_at_end", signature, kwargs)
            last_updated_start = get_input("last_updated_start", signature, kwargs)
            last_updated_end = get_input("last_updated_end", signature, kwargs)

            if created_at_start is not None or created_at_end is not None or last_updated_start is not None or last_updated_end is not None:
                timestamp_bookends_checker(
                    created_at_start,
                    created_at_end,
                    last_updated_start,
                    last_updated_end,
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

        return func(*args, **kwargs)

    setattr(wrapper, "system_base_type_checked", bool(True))

    return wrapper


def file_converters_input_check(func):
    def wrapper(*args, **kwargs):
        if "local_file_path" in kwargs:
            if kwargs["local_file_path"] is not None:
                if os.path.exists(kwargs["local_file_path"]) is False:
                    raise FileNotFoundError(f"the file '{kwargs['local_file_path']}' does not exist.")
            else:
                raise ValueError("local_file_path cannot be None")
        if "local_save_directory" in kwargs:
            if kwargs["local_save_directory"] is not None:
                if os.path.exists(kwargs["local_save_directory"]) is False:
                    raise FileNotFoundError(f"the directory '{kwargs['local_save_directory']}' does not exist.")

        if "verbose" in kwargs:
            if kwargs["verbose"] is not None:
                if not isinstance(kwargs["verbose"], bool):
                    raise ValueError("verbose is not a boolean")
            else:
                raise ValueError("verbose cannot be None")
        return func(*args, **kwargs)

    return wrapper
