from krixik.utilities.validators.system.base.use_default_clean_options import (
    use_default_clean_options_checker,
)
import pytest

test_failure_data = ["a", 1, [], {}, " ", ""]


@pytest.mark.parametrize("test_failure_data", test_failure_data)
def test_failure(test_failure_data):
    with pytest.raises((ValueError, TypeError)):
        use_default_clean_options_checker(test_failure_data)


test_success_data = [True, False]


@pytest.mark.parametrize("use_default_clean_options", test_success_data)
def test_success(use_default_clean_options):
    assert use_default_clean_options_checker(use_default_clean_options) is None
