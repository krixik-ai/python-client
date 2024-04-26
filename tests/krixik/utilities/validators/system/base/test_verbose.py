from krixik.utilities.validators.system.base.verbose import verbose_checker
import pytest

test_failure_data = [(""), ("a"), ("True"), ("False"), (1), ({"hi": "there"}), ([])]


@pytest.mark.parametrize("verbose", test_failure_data)
def test_failure(verbose):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        verbose_checker(verbose)


test_success_data = [
    (True),
    (False),
]


@pytest.mark.parametrize("verbose", test_success_data)
def test_success(verbose):
    assert verbose_checker(verbose) is None
