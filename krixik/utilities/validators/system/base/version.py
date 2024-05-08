import re


def is_valid_version_string(s: str) -> bool:
    pattern = re.compile(r"^\d+\.\d+\.\d+$")
    return bool(pattern.match(s))


def version_checker(version: str) -> None:
    if not isinstance(version, str):
        raise ValueError("version must be a string")
    if not is_valid_version_string(version):
        raise ValueError(f"version must be valid and appears d.d.d, not as input {version}")
