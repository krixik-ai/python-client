from krixik.utilities.validators.system.base.file_ids import file_ids_checker
from krixik.utilities.validators.system import MAX_FILE_ID_COUNT
from tests.utilities.decorators import capture_printed_output
import pytest
import uuid

test_failure_data = [
    ["a"],
    1,
    {},
    (),
    "",
    "a",
    uuid.uuid4(),
    [uuid.uuid4()],
    [str(uuid.uuid4()), "oh hello"],
    [str(uuid.uuid4()) for v in range(MAX_FILE_ID_COUNT + 1)],
]


@pytest.mark.parametrize("file_ids", test_failure_data)
def test_failure(file_ids):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        file_ids_checker(file_ids)


test_success_data = [
    [str(uuid.uuid4())],
    [str(uuid.uuid4()), str(uuid.uuid4())],
    [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())],
]


@pytest.mark.parametrize("file_ids", test_success_data)
def test_success(file_ids):
    assert file_ids_checker(file_ids) is None


@capture_printed_output
def file_ids_checker_printout(file_ids):
    return file_ids_checker(file_ids=file_ids)


fake_file_id = str(uuid.uuid4())
test_data = [[fake_file_id, fake_file_id]]


@pytest.mark.parametrize("file_ids", test_data)
def test_duplicates(file_ids):
    results = file_ids_checker_printout(file_ids=file_ids)
    assert "WARNING: file_ids contains duplicate entries" in results["printed_output"]
