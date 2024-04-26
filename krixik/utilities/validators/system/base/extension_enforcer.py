def pairwise_extension_checker(file_name: str, local_file_path: str) -> None:
    # check that file_name extension matches local_file_name extension
    if "." + file_name.split(".")[-1] != "." + local_file_path.split(".")[-1]:
        raise ValueError(
            f'input file_name extension must match input local_file_path extension - INFO: input file_name extension: {"." + file_name.split(".")[-1]}, input local_file_path extension: {local_file_path[-4:]}'
        )
