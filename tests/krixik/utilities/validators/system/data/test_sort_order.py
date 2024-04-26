from krixik.utilities.validators.system.base.sort_order import (
    sort_order_checker,
)
import pytest

test_failure_data = [
    "invalid_sort_order",  # string
    1,  # int
    [1, 2, 3],  # list
    {1, 2, 3},  # set
    {1: 2, 3: 4},  # dict
    "Ascending",
    "Descending",
    True,
    "True",
]


@pytest.mark.parametrize("sort_order", test_failure_data)
def test_failure(sort_order):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        sort_order_checker(sort_order)


test_success_data = [
    "ascending",  # string`
    "descending",  # string`
    "global",
]


@pytest.mark.parametrize("sort_order", test_success_data)
def test_success(sort_order):
    assert sort_order_checker(sort_order) is None

