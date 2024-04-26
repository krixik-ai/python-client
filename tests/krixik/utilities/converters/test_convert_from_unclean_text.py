from krixik.utilities.converters.unclean_to_clean_txt import (
    convert,
)
from krixik.utilities.validators.data.text import is_clean
from tests.krixik import text_files_path
import pytest
import os 

test_data = [
    (1, True),
    ([], True),
]

valid_local_save_directory = text_files_path + "test_preprocessed"
if not os.path.exists(valid_local_save_directory):
    os.makedirs(valid_local_save_directory)

@pytest.mark.parametrize("clean_options, use_default_clean_options", test_data)
def test_1(clean_options, use_default_clean_options):
    """check that clean_options and use_default_clean_options are typed checked correctly"""
    with pytest.raises((ValueError, TypeError)):
        convert(
            local_file_path=text_files_path + "1984_short_unclean.txt",
            clean_options=clean_options,
            local_save_directory=text_files_path + "test_preprocessed",
            use_default_clean_options=use_default_clean_options,
        )


test_data = [
    text_files_path + "1984_short_unclean.txt",
]


@pytest.mark.parametrize("local_file_path", test_data)
def test_2(local_file_path):
    """test that file cleaned with custom clean_options is clean"""
    # double check file contains invalid characters
    result = is_clean(
        local_file_path=local_file_path,
        minimum_word_count=10,
        minimum_file_size=0.000001,
        maximum_file_size=3.0,
    )

    # assert that 'invalid_characters' a key in result
    assert "invalid_characters" in result.keys()

    # create clean_options - remove all invalid chars
    clean_options = {v: "" for v in result["invalid_characters"]}

    # convert text to clean text
    new_local_file_path = convert(
        local_file_path=local_file_path,
        local_save_directory=text_files_path + "test_preprocessed",
        clean_options=clean_options,
        use_default_clean_options=False,
    )  # use_default_clean_options must always be False in these tests

    # assert that new file path is valid, of size, and clean
    assert is_clean(local_file_path=new_local_file_path) is None


test_data = [
    text_files_path + "1984_short_unclean.txt",
]


@pytest.mark.parametrize("local_file_path", test_data)
def test_3(local_file_path):
    """test that file cleaned with default clean options is clean"""
    # double check file contains invalid characters
    result = is_clean(
        local_file_path=local_file_path,
        minimum_word_count=10,
        minimum_file_size=0.000001,
        maximum_file_size=3.0,
    )

    # assert that 'invalid_characters' a key in result
    assert "invalid_characters" in result.keys()

    # convert text to clean text
    new_local_file_path = convert(
        local_file_path=local_file_path,
        local_save_directory=text_files_path + "test_preprocessed",
        use_default_clean_options=True,
    )  # use_default_clean_options must always be True in these tests

    # assert that new file path is valid, of size, and clean
    assert is_clean(local_file_path=new_local_file_path) is None


def test_delete_on_failure():
    """test that cleaned file is deleted when it is too large"""
    # create polluted characters that will be recursively enlarged in test file
    valid_local_save_directory = text_files_path + "test_preprocessed"
    local_file_path = text_files_path + "Little Women.txt"
    clean_options = {}
    pollute_characters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
    ]
    for p in pollute_characters:
        clean_options[p] = (
            "a" * 32
        )  # note that this replacement explicitly enlargest 1984_short_unclean.txt beyond maximum limits

    with pytest.raises((ValueError, TypeError, FileNotFoundError)) as excinfo:
        convert(
            local_file_path=local_file_path,
            local_save_directory=valid_local_save_directory,
            clean_options=clean_options,
            use_default_clean_options=False,
        )

    # next assert FileNotFoundError when attempting to read new file
    file_name = local_file_path.split("/")[-1].split(".")[0]
    converted_file_path = valid_local_save_directory + "/" + file_name + ".txt"
    with pytest.raises(FileNotFoundError):
        file = open(converted_file_path, "r")
        content = file.read(20)
