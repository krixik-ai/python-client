from krixik.utilities.validators.system.base.timestamp_bookends import (
    timestamp_bookends_checker,
)
import pytest

test_failure_data = [
    (
        1,
        "2025-01-01",
        None,
        None,
    ),
    (
        "2025-01-01",
        1,
        None,
        None,
    ),
    (
        "1",
        "2025-01-01",
        None,
        None,
    ),
    (
        "2025-01-01",
        "1",
        None,
        None,
    ),
    (
        "2025-12-32",
        "2025-01-01",
        None,
        None,
    ),
    (
        [],
        "2025-01-01",
        None,
        None,
    ),
    (
        {},
        "2025-01-01",
        None,
        None,
    ),
    (
        1.5,
        "2025-01-01",
        None,
        None,
    ),
    (
        True,
        "2025-01-01",
        None,
        None,
    ),
    (
        False,
        "2025-01-01",
        None,
        None,
    ),
    (
        "2025-01-01",
        [],
        None,
        None,
    ),
    (
        "2025-01-01",
        {},
        None,
        None,
    ),
    (
        "2025-01-01",
        1.5,
        None,
        None,
    ),
    (
        "2025-01-01",
        True,
        None,
        None,
    ),
    (
        "2025-01-01",
        False,
        None,
        None,
    ),
    (
        "2025-01-01",
        "2020-01-01",
        None,
        None,
    ),  # create_at_start too early
    (
        "2025-01-01",
        "2020-01-01",
        None,
        None,
    ),  # create_at_end too early
    (
        "2025-01-01",
        "2023-01-01",
        None,
        None,
    ),  # create_at_start > create_at_end
    (
        None,
        None,
        1,
        "2025-01-01",
    ),  # test int for last_updated_start
    (
        None,
        None,
        "2025-01-01",
        1,
    ),  # test int for last_updated_end
    (
        None,
        None,
        "1",
        "2025-01-01",
    ),  # improper string for last_updated_start
    (
        None,
        None,
        "2025-01-01",
        "1",
    ),  # improper string for last_updated_end
    (
        None,
        None,
        "2025-12-32",
        "2025-01-01",
    ),  # improper string for create_at_start
    (
        None,
        None,
        "2025-14-32",
        "2025-01-01",
    ),  # improper string for create_at_start
    (
        None,
        None,
        [],
        "2025-01-01",
    ),
    (
        None,
        None,
        {},
        "2025-01-01",
    ),
    (
        None,
        None,
        1.5,
        "2025-01-01",
    ),
    (
        None,
        None,
        True,
        "2025-01-01",
    ),
    (
        None,
        None,
        False,
        "2025-01-01",
    ),
    (
        None,
        None,
        "2025-01-01",
        [],
    ),
    (
        None,
        None,
        "2025-01-01",
        {},
    ),
    (
        None,
        None,
        "2025-01-01",
        1.5,
    ),
    (
        None,
        None,
        "2025-01-01",
        True,
    ),
    (
        None,
        None,
        "2025-01-01",
        False,
    ),
    (
        None,
        None,
        "2025-01-01",
        "2020-01-01",
    ),  # last_updated_start too early
    (
        None,
        None,
        "2025-01-01",
        "2020-01-01",
    ),  # last_updated_end too early
    (
        None,
        None,
        "2025-01-01",
        "2023-01-01",
    ),  # last_updated_start > last_updated_end
    (
        None,
        None,
        "2022-01-01 25:23:03",
        "2023-01-01",
    ),  # last_updated_start > last_updated_end
    (
        None,
        None,
        "2022-01-01 05:75:03",
        "2023-01-01",
    ),  # last_updated_start > last_updated_end
    (
        None,
        None,
        "2022-01-01 05:03:76",
        "2023-01-01",
    ),  # last_updated_start > last_updated_end
]


@pytest.mark.parametrize(
    "created_at_start, created_at_end, last_updated_start, last_updated_end",
    test_failure_data,
)
def test_failure(
    created_at_start, created_at_end, last_updated_start, last_updated_end
):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        timestamp_bookends_checker(
            created_at_start, created_at_end, last_updated_start, last_updated_end
        )


test_success_data = [
    (
        None,
        None,
        None,
        None,
    ),
    (
        "2025-01-01",
        None,
        None,
        None,
    ),
    (
        None,
        "2025-01-01",
        None,
        None,
    ),
    (
        None,
        None,
        "2025-01-01",
        None,
    ),
    (
        None,
        None,
        None,
        "2025-01-01",
    ),
    (
        "2025-01-01",
        "2025-01-01",
        None,
        None,
    ),
    (
        "2025-01-01",
        None,
        "2025-01-01",
        None,
    ),
    (
        "2025-01-01",
        None,
        None,
        "2025-01-01",
    ),
    (
        None,
        "2025-01-01",
        "2025-01-01",
        None,
    ),
    (
        None,
        "2025-01-01",
        None,
        "2025-01-01",
    ),
    (
        None,
        None,
        "2025-01-01",
        "2025-01-01",
    ),
    (
        "2025-01-01",
        "2025-01-01",
        "2025-01-01",
        None,
    ),
    (
        "2025-01-01",
        "2025-01-01",
        None,
        "2025-01-01",
    ),
    (
        "2025-01-01",
        None,
        "2025-01-01",
        "2025-01-01",
    ),
    (
        None,
        "2025-01-01",
        "2025-01-01",
        "2025-01-01",
    ),
    (
        "2025-01-01",
        "2025-01-01",
        "2025-01-01",
        "2025-01-01",
    ),
    (
        "2025-01-01 05:03:03",
        "2025-01-01 05:03:03",
        "2025-01-01 05:03:03",
        "2025-01-01 05:03:03",
    ),
    (
        "2025-01-01 05:03:03",
        "2025-01-01 05:03:03",
        "2025-01-01 05:03:03",
        "2025-01-01 05:03:03",
    ),
]


@pytest.mark.parametrize(
    "created_at_start, created_at_end, last_updated_start, last_updated_end",
    test_success_data,
)
def test_success(
    created_at_start, created_at_end, last_updated_start, last_updated_end
):
    assert (
        timestamp_bookends_checker(
            created_at_start, created_at_end, last_updated_start, last_updated_end
        )
        is None
    )
