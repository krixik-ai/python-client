from krixik.utilities.validators.system.base.lower_case import lower_case_file_names
from krixik.utilities.validators.system.base.lower_case import (
    lower_case_symbolic_directory_paths,
)
from krixik.utilities.validators.system.base.lower_case import (
    lower_case_symbolic_file_paths,
)
from krixik.utilities.validators.system.base.lower_case import lower_case_file_tags
from krixik.utilities.validators.system.base.lower_case import lower_case_decorator

import pytest

## test lower_case functions one-by-one, then test decorator ##
test_data = [["CaMeL_cAsE_nAmE.txt"], ["BOBS.docx"]]


@pytest.mark.parametrize("file_names", test_data)
def test_1(file_names):
    """test that lower_case_file_names operates correctly, verbose False - no need to test verbose True due to vprint tests"""
    lower_names = lower_case_file_names(file_names=file_names, verbose=False)
    for ind, name in enumerate(lower_names):
        assert file_names[ind].lower() == lower_names[ind]


@pytest.mark.parametrize("symbolic_directory_paths", test_data)
def test_2(symbolic_directory_paths):
    """test that lower_case_symbolic_directory_paths operates correctly, verbose False - no need to test verbose True due to vprint tests"""
    lower_names = lower_case_symbolic_directory_paths(
        symbolic_directory_paths=symbolic_directory_paths, verbose=False
    )
    for ind, name in enumerate(symbolic_directory_paths):
        assert symbolic_directory_paths[ind].lower() == lower_names[ind]


@pytest.mark.parametrize("symbolic_file_paths", test_data)
def test_3(symbolic_file_paths):
    """test that lower_case_symbolic_file_paths operates correctly, verbose False - no need to test verbose True due to vprint tests"""
    lower_names = lower_case_symbolic_file_paths(
        symbolic_file_paths=symbolic_file_paths, verbose=False
    )
    for ind, name in enumerate(symbolic_file_paths):
        assert symbolic_file_paths[ind].lower() == lower_names[ind]


test_data = [[{"kEy": "VaLuE"}], [{"KEY": "VALUE"}]]


@pytest.mark.parametrize("file_tags", test_data)
def test_4(file_tags):
    """test that lower_case_file_tags operates correctly, verbose False - no need to test verbose True due to vprint tests"""
    lower_names = lower_case_file_tags(file_tags=file_tags, verbose=False)

    # loop over file_tags lists and assert
    for lower_tag, tag in zip(lower_names, file_tags):
        # collect keys and values for set comparison
        og_key = list(tag.keys())[0]
        lower_key = list(lower_tag.keys())[0]
        og_value = list(tag.values())[0]
        lower_value = list(lower_tag.values())[0]

        # assert that key and value sets are the same
        assert set(og_key.lower()) == set(lower_key)
        assert set(og_value.lower()) == set(lower_value)

        # assure that key-value pairs align after lower-casing
        for key in list(tag.keys()):
            assert lower_tag[key.lower()] == tag[key].lower()


## test lower case decorator
test_data = [
    [
        ["CaMeL_cAsE_nAmE.txt"],
        ["CaMeL_cAsE_nAmE.txt"],
        ["CaMeL_cAsE_nAmE.txt"],
        [{"kEy": "VaLuE"}],
    ],
    [["BOBS.docx"], ["BOBS.docx"], ["BOBS.docx"], [{"KEY": "VALUE"}]],
]


@lower_case_decorator
def func(file_names, symbolic_directory_paths, symbolic_file_paths, file_tags, verbose):
    return file_names, symbolic_directory_paths, symbolic_file_paths, file_tags


@pytest.mark.parametrize(
    "file_names, symbolic_directory_paths, symbolic_file_paths, file_tags", test_data
)
def test_5(file_names, symbolic_directory_paths, symbolic_file_paths, file_tags):
    """test that lower_case decorator operates correctly, verbose False - no need to test verbose True due to vprint tests"""
    # lower case all query arguments using decorator
    (
        decorator_file_names,
        decorator_symbolic_directory_paths,
        decorator_symbolic_file_paths,
        decorator_file_tags,
    ) = func(
        file_names=file_names,
        symbolic_directory_paths=symbolic_directory_paths,
        symbolic_file_paths=symbolic_file_paths,
        file_tags=file_tags,
        verbose=False,
    )

    # lower case file_names using individual function
    lower_file_names = lower_case_file_names(file_names=file_names, verbose=False)

    # lower case symbolic_directory_paths using individual function
    lower_symbolic_directory_paths = lower_case_symbolic_directory_paths(
        symbolic_directory_paths=symbolic_directory_paths, verbose=False
    )

    # lower case symbolic_file_paths using individual function
    lower_symbolic_file_paths = lower_case_symbolic_file_paths(
        symbolic_file_paths=symbolic_file_paths, verbose=False
    )

    # lower case file_tags using individual function
    lower_tags = lower_case_file_tags(file_tags=file_tags, verbose=False)

    # assert equality between both ways of lower casing each argument type
    assert decorator_file_names == lower_file_names
    assert decorator_symbolic_directory_paths == lower_symbolic_directory_paths
    assert decorator_symbolic_file_paths == lower_symbolic_file_paths
    assert decorator_file_tags == lower_tags
