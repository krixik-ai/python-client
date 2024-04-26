def convert_paths_to_dict(paths: list[str]) -> dict[str, str]:
    root: dict[str, str] = {}
    for path in paths:
        # separate by slashes, disregarding the first `/`
        path = path.lstrip("/").split("/")
        # pop off the last key-value component
        key, _, val = path.pop(-1).partition("=")
        # find the target dict starting from the root
        target_dict = root
        for component in path:
            target_dict: dict[str, str] = target_dict.setdefault(component, {})
        # assign key-value
        target_dict[key] = val
    return root


def tree(paths: list[str], prefix: str = "") -> str:
    """
    A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """

    # prefix components:
    space = "    "
    branch = "│   "
    # pointers
    tee = "├── "
    last = "└── "

    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(paths) - 1) + [last]
    for pointer, path in zip(pointers, paths):
        if "." not in path:
            yield prefix + pointer + "/" + path
        else:
            yield prefix + pointer + path
        if isinstance(paths[path], dict):  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more │
            yield from tree(paths[path], prefix=prefix + extension)


def show_symbolic_file_tree(paths: list[str]) -> int:
    try:
        # convert paths to dict
        dict_paths = convert_paths_to_dict(paths)

        # Display root separately
        print("/")

        # Print tree of dict_paths
        for line in tree(dict_paths):
            print(line)

        return 0
    except Exception as e:
        print(f"FAILURE: show tree illustrator failed with exception {e}")
        return 1
