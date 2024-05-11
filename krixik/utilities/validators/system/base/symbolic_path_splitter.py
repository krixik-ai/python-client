def symbolic_path_splitter(symbolic_file_path: str) -> tuple:
    if not isinstance(symbolic_file_path, str):
        raise ValueError("symbolic_file_path must be a string")

    split = symbolic_file_path.split("/")
    file_name = split[-1]

    symbolic_directory_path = "/".join(split[:-1])
    if len(symbolic_directory_path) == 0:
        symbolic_directory_path = "/"
    return symbolic_directory_path, file_name
