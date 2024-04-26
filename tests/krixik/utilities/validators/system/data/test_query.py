from krixik.utilities.validators.system.base.query import query_checker
from krixik.utilities.validators import Q_MIN, Q_MAX
import pytest

test_failure_data = [
    "s" * (Q_MAX + 1),
    "s" + " " * (Q_MAX),
    "s" * (Q_MIN - 1),
    [],
    {},
    1.5,
    1,
    "",
]


@pytest.mark.parametrize("query", test_failure_data)
def test_failure(query):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        query_checker(query)


test_success_data = [
    "hi there",
    "我在滋滋作響",
]


@pytest.mark.parametrize("query", test_success_data)
def test_success(query):
    assert query_checker(query) is None
