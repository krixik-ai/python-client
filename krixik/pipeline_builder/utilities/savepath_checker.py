def savepath_check(save_path: str) -> None:
    if not isinstance(save_path, str):
        raise ValueError(f"FAILURE: config_path - {save_path} is not a string")

    try:
        file_path_ext = save_path.split(".")[-1]
    except Exception:
        raise ValueError(f"config_path - {save_path} - has no extension")

    if file_path_ext != "yml" and file_path_ext != "yaml":
        raise ValueError(f"config_path -{save_path} - must have a .yml or .yaml extension")
