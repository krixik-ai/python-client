from krixik.utilities.validators.data.text import is_valid
from krixik.utilities.validators.data.text import is_size
from krixik.utilities.validators.data.text import is_clean
from tests.krixik import text_files_path
from tests.utilities.decorators import capture_printed_output
import pytest

# first - check is_valid
test_failure_data = [
    text_files_path + "chapter_1_short.pdf",
    text_files_path + "demo.docx",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_1(local_file_path):
    """type error"""
    with pytest.raises((ValueError, TypeError)) as excinfo:
        is_valid(local_file_path=local_file_path)


test_success_data = [
    text_files_path + "my_life_and_work_short.txt",
    text_files_path + "1984_short.txt",
]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_2(local_file_path):
    """successful validation"""
    assert is_valid(local_file_path=local_file_path) is None


# second - check is_size
test_failure_data = [
    text_files_path + "Empty McFile.txt",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_3(local_file_path):
    """file too small"""
    with pytest.raises(ValueError, match=r".*current maximum size allowable\.*"):
        is_size(local_file_path=local_file_path)


# second - check is_size
test_failure_data = [
    text_files_path + "random_chars.txt",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_3_2(local_file_path):
    """file too large"""
    with pytest.raises(ValueError, match=r".*current maximum size allowable\.*"):
        is_size(local_file_path=local_file_path,
                maximum_file_size=0.5)


test_success_data = [
    text_files_path + "my_life_and_work_short.txt",
    text_files_path + "1984_short.txt",
]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_4(local_file_path):
    """is_size successful validation"""
    assert (
        is_size(
            local_file_path=local_file_path,
            minimum_word_count=10,
            minimum_file_size=0.000001,
            maximum_file_size=100.0,
        )
        is None
    )


# third - check is_clean
@capture_printed_output
def is_clean_print(
    local_file_path, minimum_word_count, minimum_file_size, maximum_file_size, verbose
):
    is_clean(
        local_file_path=local_file_path,
        minimum_word_count=minimum_word_count,
        minimum_file_size=minimum_file_size,
        maximum_file_size=maximum_file_size,
        verbose=verbose,
    )


test_failure_data = [
    text_files_path + "1984_short_unclean.txt",
]


@pytest.mark.parametrize("local_file_path", test_failure_data)
def test_5(local_file_path):
    """assert that 'invalid_characters' a key in result"""
    result = is_clean(
        local_file_path=local_file_path,
        minimum_word_count=10,
        minimum_file_size=0.000001,
        maximum_file_size=3.0,
        verbose=True,
    )

    # assert that 'invalid_characters' a key in result
    assert "invalid_characters" in result.keys()

    # test for printout
    result = is_clean_print(
        local_file_path=local_file_path,
        minimum_word_count=10,
        minimum_file_size=0.000001,
        maximum_file_size=3.0,
        verbose=True,
    )

    # check result['printed_output'] for expected printout
    assert "The following non-alpha-numeric characters" in result["printed_output"]


test_success_data = [
    text_files_path + "my_life_and_work_short.txt",
    text_files_path + "1984_short.txt",
]


@pytest.mark.parametrize("local_file_path", test_success_data)
def test_6(local_file_path):
    """is_clean successful validation"""
    assert (
        is_clean(
            local_file_path=local_file_path,
            minimum_word_count=10,
            minimum_file_size=0.000001,
            maximum_file_size=100.0,
        )
        is None
    )

    # test for printout
    result = is_clean_print(
        local_file_path=local_file_path,
        minimum_word_count=10,
        minimum_file_size=0.000001,
        maximum_file_size=3.0,
        verbose=False,
    )

    # check result['printed_output'] for expected printout
    assert len(result["printed_output"]) == 0


# check line count failure
test_data = [text_files_path + "All ones.txt"]


@pytest.mark.parametrize("local_file_path", test_data)
def test_7(local_file_path):
    """line count failure"""
    with pytest.raises(
        ValueError, match=r".*it appears that the line count is greater\.*"
    ):
        is_size(local_file_path=local_file_path, maximum_line_count=10000)


# check word count failure
test_data = [text_files_path + "a few words.txt"]


@pytest.mark.parametrize("local_file_path", test_data)
def test_8(local_file_path):
    """word count failure"""
    with pytest.raises(
        ValueError,
        match=r".*it appears that the word count is less than the allowed minimum\.*",
    ):
        is_size(local_file_path=local_file_path)
