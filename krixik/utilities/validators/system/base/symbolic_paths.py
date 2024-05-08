import copy
import re
from krixik.utilities.utilities import vprint
from krixik.utilities.validators.system.base.file_names import (
    individual_file_name_checker,
)
from krixik.utilities.validators.system import (
    SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH,
    MAX_SYMBOLIC_PATH_COUNT,
)


def lower_case_symbolic_paths(symbolic_paths: list) -> list:
    return [s.lower() for s in symbolic_paths]


# symbolic directory paths
# define pattern for valid directory path
symbolic_directory_path_valid_pattern = r"^/[a-zA-Z0-9 _-]+(?:/[a-zA-Z0-9 _-]+)*(?:/$)?$"


def is_valid_directory_path(path: str) -> bool:
    return bool(re.match(symbolic_directory_path_valid_pattern, path))


# check individual symbolic directory path
def individual_symbolic_directory_path_checker(path: str, phase: str = "other") -> None:
    if path is not None:
        # check that path is a string
        if not isinstance(path, str):
            raise TypeError(f"invalid symbolic_directory_path: not a string - {path}")

        # check that path length is greater than 0
        if len(path) == 0:
            raise ValueError(f"invalid symbolic_directory_path: length is 0 - {path}")

        # check that path length is less than SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH
        if len(path) > SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH:
            raise ValueError(f"invalid symbolic_directory_path: length is greater than 128 (current maximum length allowable) - {path}")

        # check if path ends with /
        if len(path) > 1 and path[-1] == "/":
            raise ValueError(f"invalid symbolic_directory_path: cannot end with / - {path}")

        # check if path starts with /
        if path[0] != "/":
            raise ValueError(f"invalid symbolic_directory_path: must start with / - {path}")

        # type check that path - minus possible * at the end - is a valid directory path
        test_path = copy.deepcopy(path)
        if phase != "process":
            if path[-1] == "*":
                test_path = path[:-1]
            if test_path != "/":
                res = is_valid_directory_path(test_path)
                if res is False:
                    raise ValueError(
                        f"invalid symbolic_directory_path: please check that your symbolic path takes a unix form: {symbolic_directory_path_valid_pattern} \n You can only use alphanumeric characters, spaces, underscores, dashes, and forward slashes. \n Example symbolic_diretory_path: /home/files/invoices"
                    )
        else:
            if path != "/":
                res = is_valid_directory_path(test_path)
                if res is False:
                    raise ValueError(
                        f"invalid symbolic_directory_path: please check that your symbolic path takes a unix form: {symbolic_directory_path_valid_pattern} \n You can only use alphanumeric characters, spaces, underscores, dashes, and forward slashes. \n Example symbolic_diretory_path: /home/files/invoices"
                    )
            # else:
            #     raise ValueError(
            #         f"invalid symbolic_directory_path: cannot be / - {path}"
            #     )

        # check if path contains /etc and more than two instances of '/'
        if "/etc" in path and path != "/etc/*" and path.count("/") >= 2:
            raise ValueError(f"Invalid symbolic_directory_path: cannot contain /etc - {path}")


# check symbolic directory paths
def symbolic_directory_paths_checker(symbolic_directory_paths: list, phase="other", verbose: bool = True) -> None:
    if symbolic_directory_paths is not None:
        # check that symbolic_directory_paths is a list
        if not isinstance(symbolic_directory_paths, list):
            raise TypeError("symbolic_directory_paths is not a list")

        if len(symbolic_directory_paths) == 0:
            raise ValueError("symbolic_directory_paths is empty")

        if len(symbolic_directory_paths) > MAX_SYMBOLIC_PATH_COUNT:
            raise ValueError(f"symbolic_directory_paths contains more than {MAX_SYMBOLIC_PATH_COUNT} paths - {symbolic_directory_paths}")

        # check that symbolic_directory_paths is not empty
        if symbolic_directory_paths is not None:
            # check that all paths in symbolic_directory_paths are valid paths
            for path in symbolic_directory_paths:
                # check individual path
                individual_symbolic_directory_path_checker(path, phase=phase)

            # check for duplicates
            if len(symbolic_directory_paths) != len(set(symbolic_directory_paths)):
                # find duplicates
                duplicates = []
                for path in symbolic_directory_paths:
                    if symbolic_directory_paths.count(path) > 1:
                        duplicates.append(path)

                # print error message
                vprint(
                    f"WARNING: symbolic_directory_paths contains duplicate entries - {duplicates}",
                    verbose=verbose,
                )
                vprint(
                    "INFO: You can remove duplicates by using Python's list(set()) function on your list of symbolic_directory_paths",
                    verbose=verbose,
                )
        else:
            raise ValueError("symbolic_directory_paths is None")


# symbolic file paths
def individual_symbolic_file_path_checker(file_path: str, valid_extensions: list) -> None:
    if file_path is not None:
        # check that file_path is a string
        if not isinstance(file_path, str):
            raise TypeError(f"invalid symbolic_file_path: not a string - {file_path}")

        # check that file_path has length greater than 0
        if len(file_path) == 0:
            raise ValueError("Input symbolic_file_path has length 0 - a valid file path must at least be forward slash '/' indicating root directory")

        # check that file_path starts with '/'
        if file_path[0] != "/":
            raise ValueError(f"Input symbolic_file_path did not begin with a forward slash ('/') - {file_path}")

        # split file_path into directory_path and file_name
        try:
            split = file_path.split("/")
            directory_path = "/".join(split[:-1]) if split[:-1] != [""] else "/"
            file_name = split[-1]
        except Exception as e:
            raise ValueError(f"invalid symbolic_file_path: unable to split into directory_path and file_name - {file_path} - {e}")

        try:
            # check that file_name is a valid file name
            individual_file_name_checker(file_name, valid_extensions)

            # check that directory_path is a valid directory path
            individual_symbolic_directory_path_checker(directory_path)
        except Exception as e:
            if "symbolic_directory_path" in str(e):
                raise ValueError(
                    f"the symbolic_directory_path portion - {directory_path} -  of your symbolic_file_path - {file_path} - failed with exception: {e} "
                )
            if "file_name" in str(e):
                if file_name == "*":
                    raise ValueError(
                        f"the file_name portion of your symbolic_file_path - {file_path} is an asterisk '*' which is not allowed - you can only use an asterisk at the end of a symbolic_directory_path"
                    )
                else:
                    raise ValueError(f"the file_name portion - {file_name} - of your symbolic_file_path - {file_path} - failed with exception: {e} ")


def symbolic_file_paths_checker(symbolic_file_paths: list, valid_extensions: list, verbose: bool = True) -> None:
    if symbolic_file_paths is not None:
        # check that symbolic_directory_paths is a list
        if not isinstance(symbolic_file_paths, list):
            raise TypeError("symbolic_file_paths is not a list")

        # check that symbolic_file_paths is not empty
        if len(symbolic_file_paths) == 0:
            raise ValueError("symbolic_file_paths is empty")

        if len(symbolic_file_paths) > MAX_SYMBOLIC_PATH_COUNT:
            raise ValueError(f"symbolic_file_paths contains more than {MAX_SYMBOLIC_PATH_COUNT} paths - {symbolic_file_paths}")

        # check that symbolic_directory_paths is not empty
        if symbolic_file_paths is not None:
            # check that all paths in symbolic_directory_paths are valid paths
            for path in symbolic_file_paths:
                # check individual path
                individual_symbolic_file_path_checker(path, valid_extensions)

        # check for duplicates
        if len(symbolic_file_paths) != len(set(symbolic_file_paths)):
            # find duplicates
            duplicates = []
            for path in symbolic_file_paths:
                if symbolic_file_paths.count(path) > 1:
                    duplicates.append(path)

            # print error message
            vprint(
                f"WARNING: symbolic_file_paths contains duplicate entries - {duplicates}",
                verbose=verbose,
            )
            vprint(
                "INFO: You can remove duplicates by using Python's list(set()) function on your list of symbolic_file_paths",
                verbose=verbose,
            )
