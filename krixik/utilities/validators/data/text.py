import os
from krixik.utilities.utilities import invalid_char_check
from krixik.utilities.converters.default_clean_options import default_clean_options
from krixik.utilities.utilities import vprint


def is_valid(local_file_path: str) -> None:
    try:
        # check that local_file_path is a text file
        _, file_extension = os.path.splitext(local_file_path)
        if file_extension not in [".txt"]:
            raise ValueError(f"invalid local_file_path: please check that it is a text file - {local_file_path}")

        # try to read a portion of the file content to check that it is a text file
        with open(local_file_path, "r", encoding="utf-8") as file:
            file.read(4096)

    except UnicodeDecodeError:
        raise ValueError(f"invalid local_file_path: please check that it is a text file - {local_file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"the file '{local_file_path}' does not exist.")
    except Exception as e:
        raise ValueError(f"text validation failed with exception {e}")


def is_size(
    *,
    local_file_path: str | None,
    minimum_word_count: int = 6,
    maximum_line_count: int = 100000,
    minimum_file_size: float = 0.000001,
    maximum_file_size: float = 2.000001,
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

    # compute word and line count
    def compute_word_line_count(file_path: str):
        try:
            word_count = 0
            line_count = 0
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    words = line.split()
                    word_count += len(words)
                    line_count += 1
            return word_count, line_count
        except Exception as e:
            raise ValueError(f"text word and line count calculation failed with exception {e}")

    # check size of input text file
    if local_file_path is None:
        raise ValueError("invalid local_file_path - local_file_path cannot be None")
    try:
        # check that local_file_path represents a valid text file
        is_valid(local_file_path)

        # compute file size in megabytes
        file_size = compute_size(local_file_path)

        # check that file size in megabytes is greater than minimum_file_size and less than maximum_file_size
        if file_size < minimum_file_size or file_size > maximum_file_size:
            raise ValueError(
                f"input file size is {file_size} megabytes: either less than {minimum_file_size} megabytes (current minimum size allowable) or greater than {maximum_file_size} megabytes (current maximum size allowable) - {local_file_path}"
            )

        # compute word count
        file_word_count, file_line_count = compute_word_line_count(local_file_path)

        # check that word count is greater than minimum_word_count
        if file_word_count < minimum_word_count:
            raise ValueError(f"it appears that the word count is less than the allowed minimum {minimum_word_count} words")

        # check that line count is less than maximum_line_count
        if file_line_count > maximum_line_count:
            raise ValueError(f"it appears that the line count is greater than the allowed maximum {maximum_line_count} lines")

    except ValueError as ve:
        raise ve

    except Exception as e:
        raise ValueError(f"text extraction failed with exception {e}")


def is_clean(
    *,
    local_file_path: str | None,
    minimum_word_count: int = 10,
    maximum_line_count: int = 100000,
    minimum_file_size: float = 0.000001,
    maximum_file_size: float = 3.000001,
    verbose: bool = True,
) -> dict | None:
    def check_char_ord(file_path: str | None) -> dict | None:
        if file_path is None:
            raise ValueError("invalid file_path - file_path cannot be None")

        invalid_char = set()
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line_invalid_chars = invalid_char_check(line)
                invalid_char = invalid_char.union(line_invalid_chars)

        invalid_char_list = list(invalid_char)
        invalid_char_ord = [ord(char) for char in invalid_char]
        invalid_char = sorted(invalid_char, key=lambda x: invalid_char_ord[invalid_char_list.index(x)])
        clean_options = {char: str("your alphanumeric vprintable replacement for " + "'" + char[0]) for char in invalid_char}
        if len(invalid_char) > 0:
            vprint(
                f"The following non-alpha-numeric characters --> {invalid_char} <-- were found in the file: {file_path}",
                verbose=verbose,
            )
            vprint(
                "INFO: Please clean out these characters using the .process clean_options parameter and try again",
                verbose=verbose,
            )
            vprint(
                f"INFO: this argument is a dictionary that should look like the following: clean_options={clean_options}",
                verbose=verbose,
            )
            vprint(
                "INFO: do not forget to include a valid local_save_directory with this .process call to save the cleaned file",
                verbose=verbose,
            )
            vprint(
                'INFO: a list of all detected invalid characters will be returned as a dictionary with the key "invalid_characters"',
                verbose=verbose,
            )
            vprint(
                "INFO: a set of simple default clean options is available by setting use_default_clean_options=True",
                verbose=verbose,
            )
            vprint(
                "INFO: the complete set of default options is: {default_clean_options}",
                verbose=verbose,
            )
            vprint(
                "------------------------------------------------------------------------------------------------------------------",
                verbose=verbose,
            )

            default_replacements = {}
            leftovers = []
            for v in invalid_char:
                for d in default_clean_options:
                    if v in d:
                        default_replacements[v] = default_clean_options[d]
                        break
                else:
                    leftovers.append(v)

            vprint(
                "INFO: setting use_default_clean_options=True will replace the following characters in your text with the following replacements:",
                verbose=verbose,
            )
            vprint(f"INFO: {default_replacements}", verbose=verbose)

            if len(leftovers) > 0:
                vprint(
                    "INFO: the following characters will be left as is and will need suitable replacement:",
                    verbose=verbose,
                )
                vprint(f"INFO: {leftovers}", verbose=verbose)

            # package invalid_char
            invalid_char = {"invalid_characters": invalid_char}
            return invalid_char
        else:
            return None

    # check that local_file_path is valid and is less than maximum_file_size
    is_size(
        local_file_path=local_file_path,
        minimum_word_count=minimum_word_count,
        maximum_line_count=maximum_line_count,
        minimum_file_size=minimum_file_size,
        maximum_file_size=maximum_file_size,
    )

    # check for invalid characters
    ord_vals = check_char_ord(local_file_path)

    if ord_vals is not None:
        return ord_vals
    else:
        vprint(
            "SUCCESS: File check complete, file contains all valid characters",
            verbose=verbose,
        )
        return None
