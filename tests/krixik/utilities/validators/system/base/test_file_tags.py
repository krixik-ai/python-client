from krixik.utilities.validators.system.base.file_tags import file_tags_checker
from krixik.utilities.validators.system.base.file_tags import lower_case_file_tags
from krixik.utilities.validators.system import (
    TAG_VALUE_LENGTH_MAX,
    TAG_KEY_LENGTH_MAX,
    TAGS_COUNT_MAX,
)
import pytest

test_failure_data = [
    ["this cannot be a tag"],
    [1234],
    [{"": "adventure"}],
    [{"book_category": ""}],
    [{699811: "test"}],
    [{"book_category": 5971288}],
    [{"book_author": "a" * (TAG_VALUE_LENGTH_MAX + 1)}],
    [{"a" * (TAG_KEY_LENGTH_MAX + 1), "a"}],
    [{"*": "book"}],
    [{"blah": "**"}],
    [{"tag" + str(i): "value" + str(i)} for i in range(TAGS_COUNT_MAX + 1)],
    {"book_category": "adventure"},
    [{"book_category": "adventure"}, {"book_category": "adventure"}],
    [{"book_category": "燃"}],
    {},
    [{"hi"}],
    [{"book_category": "adventure", "bae": "fox"}],
    [{"book_category": "adventure"}, {"fox"}],
]


@pytest.mark.parametrize("file_tags", test_failure_data)
def test_failure(file_tags):
    with pytest.raises((ValueError, TypeError)) as excinfo:
        file_tags_checker(file_tags)


test_success_data = [
    [{"book": "*"}],
    [{"book": "*"}, {"electronics": "*"}],
    [{"book": "*"}, {"electronics": "blah"}],
    [{"book_category": "adventure"}, {"book_category": "fox"}],
]


@pytest.mark.parametrize("file_tags", test_success_data)
def test_success(file_tags):
    assert file_tags_checker(file_tags) is None


test_data = [
    ([{"book_category": "adventure"}, {"book_author": "fox"}]),  # string
    ([{"fudge": "PoLice"}]),
    ([{"BUTTER": "nuts"}]),
    ([{"FUDGE": "NUTS"}]),
]


@pytest.mark.parametrize("file_tags", test_data)
def test_success_lower(file_tags):
    lower_file_tags = lower_case_file_tags(file_tags)
    for tag in lower_file_tags:
        for key, value in tag.items():
            assert key == key.lower()
            assert value == value.lower()
