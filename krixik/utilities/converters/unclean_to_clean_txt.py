import os
from krixik.utilities.validators.data.text import is_size
from krixik.utilities.validators.system.base.utilities.decorators import (
    file_converters_input_check,
)
from krixik.utilities.converters.default_clean_options import (
    default_clean_options,
    default_clean_keys,
)
from krixik.utilities.utilities import vprint


def delete_file(*, file_path: str, exception: str) -> None:
    if file_path is not None:
        # remove file_path file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        raise ValueError(f"there seems to be a problem with your cleaned file - file cleaning failed with exception {str(exception)}")


@file_converters_input_check
def convert(
    *,
    local_file_path: str | None,
    local_save_directory: str | None,
    clean_options: dict | None = None,
    use_default_clean_options: bool = False,
    verbose: bool = True,
) -> str | None:
    """cleans input text file, replacing un-processable characters

    Parameters
    ----------
    local_file_path : str | None
        path to local file to convert
    local_save_directory : str | None
        local directory to save converted file
    clean_options: dict | None
        user-defined dictionary of character replacements
    use_default_clean_options: bool
        flag to use default system replacement options, defaults to False
    verbose : bool, optional
        by default True

    Returns
    -------
    str | None
        if cleaning successful returns path to cleaned file
    """

    if local_file_path is None:
        raise NameError("local_file_path not defined")
    if os.path.exists(local_file_path) is False:
        raise FileNotFoundError(f"the file '{local_file_path}' does not exist.")
    if local_save_directory is None:
        raise NameError("local_save_directory is not defined")

    new_file_path = ""
    try:
        # new file to write to
        file_name = "krixik_cleaned_version_" + os.path.splitext(os.path.basename(local_file_path))[0]
        extension = ".txt"
        new_file_path = os.path.join(local_save_directory, file_name + extension)

        # remove file if it already exists
        if os.path.exists(new_file_path):
            os.remove(new_file_path)

        # check that input file is a valid text file and sized correctly
        is_size(local_file_path=local_file_path)

        if clean_options is not None:
            keys = set(list(clean_options.keys()))
            values = set(list(clean_options.values()))
            intersection = keys.intersection(values)
            if len(intersection) > 0:
                raise ValueError(f"clean_options contains the same key and value: {intersection}")

        # if clean_options length greater than 0 convert to one dict
        clean_keys = []

        if clean_options is not None:
            if len(clean_options) > 0:
                clean_keys = list(clean_options.keys())
                if use_default_clean_options is True:
                    vprint(
                        "WARNING: You are using both default_clean_options and your custom clean_options.  Note: any duplication in your clean_options will overwrite the same key in default_clean_options.",
                        verbose=verbose,
                    )

        # clean file
        clean_count = 0
        line_count = 0
        with open(local_file_path, "r", encoding="utf-8") as file:
            for line in file:
                new_line = ""
                for char in line:
                    new_char = char
                    # replace char with clean_options[char] if char in clean_options
                    if clean_options is not None:
                        if len(clean_options) > 0:
                            if char in clean_keys:
                                new_char = clean_options[char]
                                clean_count += 1

                    # replace char with default_clean_options[char] if char in default_clean_options
                    if use_default_clean_options is True:
                        if char in default_clean_keys:
                            new_char = default_clean_options[char]
                            clean_count += 1

                    new_line += new_char

                # write line to new file
                if line_count == 0:
                    with open(new_file_path, "a", encoding="utf-8") as new_file:
                        new_file.write(new_line)

                if line_count > 0:
                    if os.path.exists(new_file_path):
                        with open(new_file_path, "a", encoding="utf-8") as new_file:
                            new_file.write(new_line)
                    else:
                        raise FileNotFoundError(f"file {new_file_path} does not exist")

                # check size to make sure file is not oversize - every 50 lines
                if line_count % 50 == 0 and line_count > 0:
                    is_size(local_file_path=new_file_path)

                # update counter
                line_count += 1

        if clean_count == 0:
            vprint(
                f"INFO: No characters needed cleaning from the original file: {local_file_path}",
                verbose=verbose,
            )
            vprint(
                f"INFO: Removing newly created (redundant) clean file: {new_file_path}",
                verbose=verbose,
            )
            os.remove(new_file_path)
            return local_file_path
        else:
            vprint(
                f"SUCCESS: File cleaning complete, result saved to: {new_file_path}",
                verbose=verbose,
            )

            vprint(
                "INFO: Checking that file size falls within acceptable parameters...",
                verbose=verbose,
            )
            is_size(local_file_path=new_file_path)
            vprint("INFO:...success!", verbose=verbose)
            return new_file_path
    except ValueError as ve:
        vprint(
            "INFO:...failure!  The converted (text) file does not fall within acceptable size parameters.",
            verbose=verbose,
        )
        delete_file(file_path=new_file_path, exception=str(ve))
    except Exception as e:
        raise ValueError(f"file cleaning failed with exception: {e}")
