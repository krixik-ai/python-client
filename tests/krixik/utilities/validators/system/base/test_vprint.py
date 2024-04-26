from krixik.utilities.utilities import vprint
import pytest

test_failure_data = [
    ("a", "b"),
    ("a", None),
    ("a", 1),
    (1, True),
    ("a", "True"),
    ("a", None),
]


@pytest.mark.parametrize("message, verbose", test_failure_data)
def test_1(message, verbose):
    with pytest.raises(TypeError):
        vprint(message, verbose=verbose)


test_success_data = [
    ("a", False),
    ("a", True),
]


@pytest.mark.parametrize("message, verbose", test_success_data)
def test_2(message, verbose):
    assert vprint(message, verbose=verbose) is None
