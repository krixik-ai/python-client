import inspect
from functools import wraps
from krixik.modules.utilities.module_selections import (
    pipeline_selection_setup,
)
from krixik.utilities.utilities import get_input
from krixik.utilities.utilities import vprint
from krixik.modules.utilities.io_validator import is_valid as is_valid_json_input


def type_check_inputs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            signature = inspect.signature(func)
            self_arg = args[0] if args and hasattr(args[0], "__dict__") else None

            # confirm and hydrate module chain
            pipeline_ordered_modules = self_arg.module_chain if self_arg else kwargs["pipeline_ordered_modules"]
            modules = get_input("modules", signature, kwargs)
            verbose = get_input("verbose", signature, kwargs, default_value=True)
            hydrated_modules = pipeline_selection_setup(pipeline_ordered_modules, modules)
            kwargs["modules"] = hydrated_modules

            if "local_file_path" in list(kwargs.keys()):
                local_file_path = get_input("local_file_path", signature, kwargs)
                is_valid_json_input(pipeline_ordered_modules[0], local_file_path)

            if modules != hydrated_modules:
                vprint(
                    f"INFO: hydrated input modules: {hydrated_modules}",
                    verbose=verbose,
                )

        except ValueError as e:
            raise e
        except TypeError as e:
            raise e
        except FileNotFoundError as e:
            raise e
        except PermissionError as e:
            raise e
        except Exception as e:
            raise e

        return func(self_arg, *args[1:], **kwargs)

    setattr(wrapper, "module_selection_type_checked", bool(True))
    return wrapper
