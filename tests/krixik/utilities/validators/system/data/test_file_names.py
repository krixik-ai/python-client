from krixik.utilities.validators.system.data.text.file_names import (
    file_names_checker,
)
import pytest

# test 'process' phase first
test_failure_data = [
    {"bobs your uncle"},
    [],
    ["blah.file"],
    ["/applejuice*"],
    ["*blah.html"],
    ["*blah."],
    ["*blah"],
    ["peanut>butter*"],
    ["*燃*"],
    ["*apple", "bannana*"],
    ["water*fudge*"],
    ["water*fudge"],
    ["*water*fudge"],
    ["water*fudge*icicle"],
    ["**"],
    ["***"],
    ["**word"],
    ["my*!22"],
    ["blah.mp3"],
    ["my_life_and_work_full"],
    ["my_life_and_work_full.abc"],
]


@pytest.mark.parametrize("file_names", test_failure_data)
def test_failure_process(file_names):
    with pytest.raises((ValueError, TypeError)):
        file_names_checker(file_names, phase="process")


test_success_data = [
    ["*bakery*"],
    ["*bak,ry*"],
    ["*blah.txt"],
    ["*apple.txt", "bannana*"],
    ["*apple*", "bannana*", "blah.txt"],
    ["*apple*", "bannana*", "blah.txt", "*grape.txt"],
    ["*.txt"],
]


@pytest.mark.parametrize("file_names", test_success_data)
def test_success_process(file_names):
    assert file_names_checker(file_names, phase="other") is None


# test 'process' phase next
test_success_data = [["blah.txt"], ["blah.pptx"], ["blah.docx"], ["blah.pdf"]]


@pytest.mark.parametrize("file_names", test_failure_data)
def test_failure_upload(file_names):
    with pytest.raises((ValueError, TypeError)):
        file_names_checker(file_names, phase="process")


test_failure_data = [
    ["blah.file"],
    ["blah.html"],
    ["blah.mp3"],
    ["my_life_and_work_full.abc"],
    ["*blah.txt"],
    ["*apple*", "bannana*"],
]


@pytest.mark.parametrize("file_names", test_success_data)
def test_success_upload(file_names):
    assert file_names_checker(file_names, phase="process") is None
