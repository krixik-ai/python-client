import inspect
from functools import wraps
from krixik.utilities.utilities import vprint
from krixik.utilities.validators.system.base.verbose import verbose_checker
from krixik.utilities.utilities import get_input
from typing import Callable


# lower case an individual file_name
def lower_case_file_name(*, file_name: str, verbose: bool) -> str:
    if file_name is not None:
        lower_case_name = file_name.lower()
        if lower_case_name != file_name:
            vprint(
                f"INFO: lower casing file_name {file_name} to {lower_case_name}",
                verbose=verbose,
            )
        file_name = lower_case_name
    return file_name


# lower-case file_names
def lower_case_file_names(*, file_names: list, verbose: bool) -> list:
    if file_names is not None:
        # lower case
        lower_case_names = [lower_case_file_name(file_name=v, verbose=verbose) for v in file_names]

        # replace
        file_names = lower_case_names
    return file_names


# lower-case symbolic_directory_path
def lower_case_symbolic_directory_path(*, symbolic_directory_path: str, verbose: bool) -> str:
    if symbolic_directory_path is not None:
        lower_case_name = symbolic_directory_path.lower()
        if lower_case_name != symbolic_directory_path:
            vprint(
                f"INFO: lower casing symbolic_directory_path {symbolic_directory_path} to {lower_case_name}",
                verbose=verbose,
            )
        symbolic_directory_path = lower_case_name
    return symbolic_directory_path


# lower-case symbolic_directory_paths
def lower_case_symbolic_directory_paths(*, symbolic_directory_paths: list, verbose: bool) -> list:
    if symbolic_directory_paths is not None:
        # lower case
        lower_case_names = [lower_case_symbolic_directory_path(symbolic_directory_path=v, verbose=verbose) for v in symbolic_directory_paths]

        # replace
        symbolic_directory_paths = lower_case_names
    return symbolic_directory_paths


# lower-case symbolic_file_path
def lower_case_symbolic_file_path(*, symbolic_file_path: str, verbose: bool) -> str:
    if symbolic_file_path is not None:
        lower_case_name = symbolic_file_path.lower()
        if lower_case_name != symbolic_file_path:
            vprint(
                f"INFO: lower casing symbolic_file_path {symbolic_file_path} to {lower_case_name}",
                verbose=verbose,
            )
        symbolic_file_path = lower_case_name
    return symbolic_file_path


# lower-case symbolic_file_paths
def lower_case_symbolic_file_paths(*, symbolic_file_paths: list, verbose: bool) -> list:
    if symbolic_file_paths is not None:
        # lower case
        lower_case_names = [lower_case_symbolic_file_path(symbolic_file_path=v, verbose=verbose) for v in symbolic_file_paths]

        # replace
        symbolic_file_paths = lower_case_names
    return symbolic_file_paths


# lower case file_tags
def lower_case_file_tags(*, file_tags: list, verbose: bool) -> list:
    if file_tags is not None:
        # lower case all tags
        lower_case_tags = []
        for file_tag in file_tags:
            key = list(file_tag.keys())[0]
            value = file_tag[key]
            lower_file_tag = {key.lower(): value.lower()}
            lower_case_tags.append(lower_file_tag)

        # loop over and compare
        for lower_tag, or_tag in zip(lower_case_tags, file_tags):
            if lower_tag != or_tag:
                vprint(
                    f"INFO: lower casing file tag {or_tag} to {lower_tag}",
                    verbose=verbose,
                )

        # set file_tags to lower_case_tags
        file_tags = lower_case_tags
    return file_tags


def lower_case_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get name of function being called
        signature = inspect.signature(func)

        # Check each argument based on its name
        try:
            verbose = get_input("verbose", signature, kwargs, default_value=True)

            verbose_checker(verbose)

            # instantiate query args
            file_names = None
            file_name = None
            symbolic_directory_paths = None
            symbolic_directory_path = None
            symbolic_file_paths = None
            symbolic_file_path = None
            file_tags = None

            # loop over and lower-case required query args
            for arg_name, arg_value in kwargs.items():
                if arg_name.startswith("_"):
                    continue  # Skip special parameters (e.g., '_self', '_cls')
                if arg_name == "file_names":
                    file_names = lower_case_file_names(file_names=arg_value, verbose=verbose)
                    kwargs["file_names"] = file_names
                if arg_name == "file_name":
                    file_name = lower_case_file_name(file_name=arg_value, verbose=verbose)
                    kwargs["file_name"] = file_name
                if arg_name == "symbolic_directory_paths":
                    symbolic_directory_paths = lower_case_symbolic_directory_paths(symbolic_directory_paths=arg_value, verbose=verbose)
                    kwargs["symbolic_directory_paths"] = symbolic_directory_paths
                if arg_name == "symbolic_directory_path":
                    symbolic_directory_path = lower_case_symbolic_directory_path(symbolic_directory_path=arg_value, verbose=verbose)
                    kwargs["symbolic_directory_path"] = symbolic_directory_path
                if arg_name == "symbolic_file_paths":
                    symbolic_file_paths = lower_case_symbolic_file_paths(symbolic_file_paths=arg_value, verbose=verbose)
                    kwargs["symbolic_file_paths"] = symbolic_file_paths
                if arg_name == "symbolic_file_path":
                    symbolic_file_path = lower_case_symbolic_file_path(symbolic_file_path=arg_value, verbose=verbose)
                    kwargs["symbolic_file_path"] = symbolic_file_path
                if arg_name == "file_tags":
                    file_tags = lower_case_file_tags(file_tags=arg_value, verbose=verbose)
                    kwargs["file_tags"] = file_tags

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

    setattr(wrapper, "lower_cased", bool(True))
    return wrapper
