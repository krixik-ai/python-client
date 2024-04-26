from krixik.utilities.validators.system import (
    SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH,
    MAX_SYMBOLIC_PATH_COUNT,
    MAX_FILE_NAME_LENGTH,
)
from krixik.utilities.validators.system.base.symbolic_paths import (
    symbolic_directory_paths_checker,
    symbolic_file_paths_checker,
)
from tests.utilities.decorators import capture_printed_output
import pytest


test_failure_data = [
    [123],
    [{}],
    "/not/a/path//to/anywhere",
    ["/not/a/path//to/anywhere"],
    ["/*"],
    ["/a/path/to/somewhere/file.txt"],
    ["a" * (SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH + 1)],
    [
        "smuw5n7589wnycg4hw5ugnethgenutgn4hcguwimct54ofhuwng gh358g 4huvi4og4wug 54vnt4rigv4h r403 ghhjgtgi h4t0g"
    ],
    [""],
    ["/end/with/slash/"],
    ["/home/books/fic>tion/drama"],
    ["/home/books/fic燃tion/drama"],
    ["/etc/books"],  # no building under /etc permitted
    ["/hi/there/file.txt"],
    ["/hi/there/", "hi/there/file.txt"],
    ["/hi/there/" * (MAX_SYMBOLIC_PATH_COUNT + 1)],
    ["/home/testfiles/sobredosis//theOneLiner.txt"],
]


@pytest.mark.parametrize("symbolic_directory_paths", test_failure_data)
def test_failure_1(symbolic_directory_paths):
    """failure tests for symbolic directory paths in process phase"""
    with pytest.raises((ValueError, TypeError)) as excinfo:
        symbolic_directory_paths_checker(symbolic_directory_paths, phase="process")


test_success_data = [
    ["/a/path/to/somewhere"],
    ["/"],
]


@pytest.mark.parametrize("symbolic_directory_paths", test_success_data)
def test_success_1(symbolic_directory_paths):
    """failure tests for symbolic directory paths in process phase"""
    assert (
        symbolic_directory_paths_checker(symbolic_directory_paths, phase="process")
        is None
    )


# process phase process data - can include wildcard stumps
test_failure_data = [
    [123],
    [{}],
    "/not/a/path//to/anywhere",
    ["/not/a/path//to/anywhere"],
    ["/a/path/to/somewhere/file.txt"],
    [
        "smuw5n7589wnycg4hw5ugnethgenutgn4hcguwimct54ofhuwng gh358g 4huvi4og4wug 54vnt4rigv4h r403 ghhjgtgi h4t0g"
    ],
    [""],
]


@pytest.mark.parametrize("symbolic_directory_paths", test_failure_data)
def test_failure_2(symbolic_directory_paths):
    """failure tests for symbolic directory paths in other phase"""
    with pytest.raises((ValueError, TypeError)) as excinfo:
        symbolic_directory_paths_checker(symbolic_directory_paths, phase="other")


test_success_data = [
    ["/a/path/to/somewhere"],
    ["/"],
    ["/*"],
]


@pytest.mark.parametrize("symbolic_directory_paths", test_success_data)
def test_success_2(symbolic_directory_paths):
    """success tests for symbolic directory paths in other phase"""
    assert (
        symbolic_directory_paths_checker(symbolic_directory_paths, phase="other")
        is None
    )


@capture_printed_output
def symbolic_directory_paths_printout(symbolic_directory_paths):
    return symbolic_directory_paths_checker(
        symbolic_directory_paths=symbolic_directory_paths
    )


fake_symbolic_directory_paths = "/a/path"
test_data = [[fake_symbolic_directory_paths, fake_symbolic_directory_paths]]


@pytest.mark.parametrize("symbolic_directory_paths", test_data)
def test_duplicates(symbolic_directory_paths):
    """warning tests for symbolic directory path duplicates in process"""
    results = symbolic_directory_paths_printout(
        symbolic_directory_paths=symbolic_directory_paths
    )
    assert (
        "WARNING: symbolic_directory_paths contains duplicate entries"
        in results["printed_output"]
    )


test_failure_data = [
    ["/*"],
    [
        "/"
        + "a" * (SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH - 1)
        + "/"
        + "a" * (MAX_FILE_NAME_LENGTH - 1)
        + ".txt"
    ],
    ["/"],
]


@pytest.mark.parametrize("symbolic_file_paths", test_failure_data)
def test_failure_3(symbolic_file_paths):
    """failure tests for symbolic file paths"""
    with pytest.raises((ValueError, TypeError)) as excinfo:
        symbolic_file_paths_checker(symbolic_file_paths, valid_extensions=[".txt"])


test_success_data = [
    ["/a/path/to/somewhere/hello.txt"],
    ["/yay.txt"],
]


@pytest.mark.parametrize("symbolic_file_paths", test_success_data)
def test_success_3(symbolic_file_paths):
    """failure tests for symbolic directory paths in process phase"""
    assert (
        symbolic_file_paths_checker(symbolic_file_paths, valid_extensions=[".txt"])
        is None
    )
