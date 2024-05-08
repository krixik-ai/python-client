import os
import json


def is_valid(local_file_path: str) -> bool | None:
    try:
        # Read the content of the JSON file and load it
        with open(local_file_path, "r") as file:
            json_object = json.load(file)

        # Check if the loaded object is a dictionary
        if isinstance(json_object, list):
            # check that json_object has at least one key
            if len(json_object) < 1:
                raise ValueError("JSON file does not represent a dictionary.")
            for v in json_object:
                if not isinstance(v, dict):
                    raise ValueError("JSON file does not represent a dictionary.")
            return True
        else:
            raise ValueError("JSON file does not represent a dictionary.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file - your file is not a valid JSON file: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{local_file_path}' does not exist.")
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")


def is_size(
    *,
    local_file_path: str,
    snippet_min_token_count: int = 1,
    snippet_max_token_count: int = 255,
    snippet_max_key_length: int = 255,
    snippet_max_count: int = 1000000,
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

    # compute snippet token length and count
    def compute_snippet_size(file_path: str):
        try:
            minimum_token_count = 1
            minimum_token_count_key_value = {}
            maximum_token_count = 0
            maximum_token_count_key_value = {}
            maximum_key_length = 0
            largest_key = ""
            with open(file_path, "r") as file:
                data = json.load(file)
                snippet_count = len(data)
                for datapoint in data:
                    counter = 0
                    for key, value in datapoint.items():
                        try:
                            if len(key) > maximum_key_length:
                                maximum_key_length = len(key)
                                largest_key = key
                            if isinstance(value, str):
                                token_count = len(value.split())
                                if counter == 0:
                                    minimum_token_count = token_count
                                    maximum_token_count = token_count
                                    minimum_token_count_key_value = {key: value}
                                    maximum_token_count_key_value = {key: value}

                                if token_count > maximum_token_count:
                                    maximum_token_count = len(value.split())
                                    maximum_token_count_key_value = {key: value}

                                if token_count < minimum_token_count:
                                    minimum_token_count = token_count
                                    minimum_token_count_key_value = {key: value}

                                if len(value.strip()) == 0:
                                    minimum_token_count = 0
                                    minimum_token_count_key_value = {key: value}
                            counter += 1
                        except Exception as e:
                            raise ValueError(f"snippet token and count calculation failed on key-value pair {key}-{value} with exception {e}")

                return (
                    maximum_key_length,
                    largest_key,
                    minimum_token_count,
                    maximum_token_count,
                    snippet_count,
                    minimum_token_count_key_value,
                    maximum_token_count_key_value,
                )
        except Exception as e:
            raise ValueError(f"snippet token and count calculation failed with exception {e}")

    try:
        # check that local_file_path represents a valid json file
        is_valid(local_file_path)

        # check size of input json file
        file_size = compute_size(local_file_path)
        if file_size < minimum_file_size or file_size > maximum_file_size:
            raise ValueError(
                f"input file size is {file_size} megabytes: either less than {minimum_file_size} megabytes (current minimum size allowable) or greater than {maximum_file_size} megabytes (current maximum size allowable) - {local_file_path}"
            )

        (
            maximum_key_length,
            largest_key,
            minimum_token_count,
            maximum_token_count,
            snippet_count,
            minimum_token_count_key_value,
            maximum_token_count_key_value,
        ) = compute_snippet_size(local_file_path)

        if maximum_key_length > snippet_max_key_length:
            raise ValueError(
                f"too long key - the following key {largest_key} is too long (at present the maximum is {snippet_max_key_length} - please check this key in your input local_file_path {local_file_path}"
            )

        if snippet_count > snippet_max_count:
            raise ValueError(
                f"there are too many key-value pairs in your input local_file_path {local_file_path} - total count must be less than {snippet_max_count}"
            )
        if minimum_token_count < snippet_min_token_count:
            raise ValueError(
                f"too few tokens - the value in the following key-value pair {minimum_token_count_key_value} has too few tokens (at present the minimum is {snippet_min_token_count} - please check this key-value pair in your input local_file_path {local_file_path}"
            )
        if maximum_token_count > snippet_max_token_count:
            raise ValueError(
                f"too many tokens - the value in the following key-value pair {maximum_token_count_key_value} has too many tokens (at present the minimum is {snippet_max_token_count} - please check this key-value pair in your input local_file_path {local_file_path}"
            )

    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"invalid local_file_path: {e}")
