from krixik.utilities.validators.system.base.expire_time import expire_time_checker
from krixik.utilities.validators.system import EXPIRE_TIME_MIN, EXPIRE_TIME_MAX
import pytest

test_failure_data = [
    "s",
    (),
    [],
    {},
    1,
    True,
    EXPIRE_TIME_MIN + 0.1,
    EXPIRE_TIME_MIN - 1,
    EXPIRE_TIME_MAX + 1,
]


@pytest.mark.parametrize("expire_time", test_failure_data)
def test_failure(expire_time):
    with pytest.raises((ValueError, TypeError)):
        expire_time_checker(expire_time)


test_success_data = [
    EXPIRE_TIME_MIN + 1,
    EXPIRE_TIME_MAX - 1,
]


@pytest.mark.parametrize("expire_time", test_success_data)
def test_success(expire_time):
    assert expire_time_checker(expire_time) is None
