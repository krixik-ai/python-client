from krixik.utilities.validators.system import (
    MAX_FILE_NAME_LENGTH,
    MAX_FILE_NAME_COUNT,
)
from krixik.utilities.validators.system.base.file_names import file_names_checker
from tests.utilities.decorators import capture_printed_output
import pytest

# test 'process' phase first
test_failure_data = [
    ["a" * (MAX_FILE_NAME_LENGTH + 1)],
    ["a"],
    ["hess:word"],
    ["hello?world"],
    {"bobs your uncle"},
    [],
    ["/applejuice*"],
    ["*blah."],
    ["*blah"],
    ["peanut>butter*"],
    ["*燃*"],
    ["*apple"],
    ["water*fudge*"],
    ["water*fudge"],
    ["*water*fudge"],
    ["water*fudge*icicle"],
    ["**"],
    ["***"],
    ["**word"],
    ["my*!22"],
    1,
    ["fine.file" for v in range(MAX_FILE_NAME_COUNT + 1)],
]


@pytest.mark.parametrize("file_names", test_failure_data)
def test_failure_process(file_names):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        file_names_checker(file_names, phase="process")


test_success_data = [["*bakery*"], ["*bak,ry*"]]


@pytest.mark.parametrize("file_names", test_success_data)
def test_success_process(file_names):
    assert file_names_checker(file_names, phase="request") is None


# test 'process' phase next
valid_extensions = [".file", ".html", ".mp3"]

test_failure_data = [
    ["my_life_and_work_full.abc"],
    ["*blah.txt"],
    ["*apple*", "bannana*"],
]


@pytest.mark.parametrize("file_names", test_failure_data)
def test_failure_upload(file_names):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        file_names_checker(
            file_names, valid_extensions=valid_extensions, phase="process"
        )


test_success_data = [
    ["blah.file"],
    ["blah.html"],
    ["blah.mp3"],
]


@pytest.mark.parametrize("file_names", test_success_data)
def test_success_upload(file_names):
    assert (
        file_names_checker(
            file_names, valid_extensions=valid_extensions, phase="process"
        )
        is None
    )


@capture_printed_output
def file_names_checker_printout(file_names):
    return file_names_checker(file_names=file_names, valid_extensions=valid_extensions)


test_data = [["blah.file", "blah.file"]]


@pytest.mark.parametrize("file_names", test_data)
def test_duplicates(file_names):
    results = file_names_checker_printout(file_names=file_names)
    assert "WARNING: file_names contains duplicate entries" in results["printed_output"]
