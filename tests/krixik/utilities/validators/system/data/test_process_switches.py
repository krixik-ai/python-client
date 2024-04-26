from krixik.utilities.validators.system.base.process_switches import (
    process_switches_checker,
)
import pytest

test_failure_data = [
    ("a", "b"),
    ("True", "False"),
    (False, False),
    (1, 1),
]


@pytest.mark.parametrize(
    "process_for_keyword_search, process_for_vector_search", test_failure_data
)
def test_failure(process_for_keyword_search, process_for_vector_search):
    with pytest.raises((ValueError, TypeError)):
        process_switches_checker(
            process_for_keyword_search=process_for_keyword_search,
            process_for_vector_search=process_for_vector_search,
        )


test_success_data = [
    (True, True),
    (True, False),
    (False, True),
]


@pytest.mark.parametrize(
    "process_for_keyword_search, process_for_vector_search", test_success_data
)
def test_success(process_for_keyword_search, process_for_vector_search):
    assert (
        process_switches_checker(
            process_for_keyword_search=process_for_keyword_search,
            process_for_vector_search=process_for_vector_search,
        )
        is None
    )
