from krixik.utilities.validators.system.base.request_id import request_id_checker
import pytest
import uuid

test_failure_data = [
    ["a"],
    1,
    {},
    (),
    "",
    "a",
]


@pytest.mark.parametrize("request_id", test_failure_data)
def test_failure(request_id):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        request_id_checker(request_id)


test_success_data = [
    str(uuid.uuid4()),
]


@pytest.mark.parametrize("request_id", test_success_data)
def test_success(request_id):
    assert request_id_checker(request_id) is None
