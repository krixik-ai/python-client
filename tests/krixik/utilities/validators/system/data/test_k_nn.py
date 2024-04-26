from krixik.utilities.validators.system.base.k_nn import k_checker
from krixik.utilities.validators import K_MAX, K_MIN
import pytest


test_failure_data = [
    "hi",
    1234,
    "",
    K_MIN - 1,
    K_MAX + 1,
    -1,
    7.53,
]


@pytest.mark.parametrize("k", test_failure_data)
def test_failure(k):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        k_checker(k)


test_success_data = [
    K_MIN,
    K_MAX,
]


@pytest.mark.parametrize("k", test_success_data)
def test_success(k):
    assert k_checker(k) is None
