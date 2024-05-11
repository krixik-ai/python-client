from typing import List


def get_all_key_paths(dictionary: dict, parent_key: str = "", separator: str = ".") -> List[str]:
    key_paths = []
    for key, value in dictionary.items():
        current_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            key_paths.extend(get_all_key_paths(value, current_key, separator))
        else:
            key_paths.append(current_key)
    return key_paths


def find_value_by_path(dictionary: dict, target_path: str, separator=".") -> dict | None:
    keys = target_path.split(separator)
    current = dictionary
    for key in keys:
        if key in current:
            current = current[key]
        else:
            return None
    return current


def find_key_path_with_type(nested_dict: dict, target_key: str, current_path=None) -> list | None:
    if current_path is None:
        current_path = []

    for key, value in nested_dict.items():
        current_path.append((key, type(value)))  # Store key and its type
        if key == target_key:
            return current_path.copy()
        if isinstance(value, dict):
            found_path = find_key_path_with_type(value, target_key, current_path)
            if found_path:
                return found_path
        current_path.pop()
    return None


def find_key_paths_with_prefix_with_type(nested_dict: dict, target_prefix: str, current_path=None) -> dict | None:
    if current_path is None:
        current_path = []

    paths = []
    for key, value in nested_dict.items():
        current_path.append((key, type(value)))  # Store key and its type
        if key.startswith(target_prefix):
            paths.append(current_path.copy())
        if isinstance(value, dict):
            found_paths = find_key_paths_with_prefix(value, target_prefix, current_path)
            paths.extend(found_paths)
        current_path.pop()
    return paths
