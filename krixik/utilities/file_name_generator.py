import string
import random


def generate_random_file_name(extension: str) -> str:
    if not extension:
        raise ValueError("Extension cannot be empty")
    if not isinstance(extension, str):
        raise ValueError("Extension must be a string")

    num_chars = 10
    characters = string.ascii_letters.lower()
    random_chars = "".join(random.choice(characters) for _ in range(num_chars))
    file_name = f"{random_chars}.{extension}"
    filename = "krixik_generated_file_name_" + file_name
    return filename
