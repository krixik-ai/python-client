from krixik.utilities.validators.system.base.wait_for_process import (
    wait_for_process_checker,
)
import pytest

test_failure_data = [(""), ("a"), ("True"), ("False"), (1), ({"hi": "there"}), ([])]


@pytest.mark.parametrize("verbose", test_failure_data)
def test_failure(verbose):
    with pytest.raises((ValueError, TypeError)):
        wait_for_process_checker(verbose)


test_success_data = [
    (True),
    (False),
]


@pytest.mark.parametrize("verbose", test_success_data)
def test_success(verbose):
    assert wait_for_process_checker(verbose) is None
