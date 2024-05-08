from functools import wraps


allowed_args_dict = {
    "init": {"api_key", "api_url"},
    "delete": {"file_id"},
    "list": {
        "file_ids",
        "file_names",
        "symbolic_directory_paths",
        "symbolic_file_paths",
        "file_tags",
        "sort_order",
        "max_files",
        "created_at_start",
        "created_at_end",
        "last_updated_start",
        "last_updated_end",
        "verbose",
    },
    "fetch_output": {"file_id", "local_save_directory"},
    "update": {
        "file_id",
        "file_name",
        "symbolic_directory_path",
        "symbolic_file_path",
        "file_tags",
        "file_description",
        "expire_time",
        "verbose",
    },
    "process": {
        "file_id",
        "file_name",
        "symbolic_directory_path",
        "symbolic_file_path",
        "local_file_path",
        "file_tags",
        "file_description",
        "modules",
        "expire_time",
        "verbose",
        "wait_for_process",
        "local_save_directory",
        "og_local_file_path",
    },
    "show_tree": {"symbolic_directory_path", "max_files", "verbose"},
    "process_status": {"request_id"},
    "keyword_search": {
        "query",
        "file_ids",
        "file_names",
        "symbolic_directory_paths",
        "symbolic_file_paths",
        "file_tags",
        "sort_order",
        "max_files",
        "created_at_start",
        "created_at_end",
        "last_updated_start",
        "last_updated_end",
        "verbose",
    },
    "semantic_search": {
        "query",
        "file_ids",
        "file_names",
        "symbolic_directory_paths",
        "symbolic_file_paths",
        "file_tags",
        "sort_order",
        "max_files",
        "created_at_start",
        "created_at_end",
        "last_updated_start",
        "last_updated_end",
        "verbose",
        "k",
    },
}


def kwargs_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        if func_name == "converter_wrapper":
            func_name = "process"
        allowed_args = allowed_args_dict.get(func_name)
        if allowed_args is None:
            raise ValueError(f"function not supported: '{func_name}'")

        unexpected_args = set(kwargs.keys()) - allowed_args
        if unexpected_args:
            raise TypeError(f"unexpected keyword argument(s) for '{func_name}': {', '.join(unexpected_args)}")
        return func(*args, **kwargs)

    return wrapper
