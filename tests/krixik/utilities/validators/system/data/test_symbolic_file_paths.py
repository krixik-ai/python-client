from krixik.utilities.validators.system import (
    MAX_FILE_NAME_LENGTH,
    SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH,
    MAX_SYMBOLIC_PATH_COUNT,
)
from krixik.utilities.validators.system.base.symbolic_paths import (
    symbolic_file_paths_checker,
)
import pytest
valid_extensions = [".txt"]

# check 'process' phase first
test_failure_data = [
    [123],
    [{}],
    "/not/a/path//to/anywhere",
    ["/not/a/path//to/anywhere/test.txt"],
    ["/"],
    ["/*"],
    [
        "smuw5n7589wnycg4hw5ugnethgenutgn4hcguwimct54ofhuwng gh358g 4huvi4og4wug 54vnt4rigv4h r403 ghhjgtgi h4t0g"
    ],
    ["/etc/blah/test.txt"],  # no building under /etc permitted
    [""],
    ["/hi/there/file.txt" * (MAX_SYMBOLIC_PATH_COUNT + 1)],
    [
        "/a" * SYMBOLIC_DIRECTORY_PATH_MAX_LENGTH
        + "/"
        + "a" * MAX_FILE_NAME_LENGTH
        + ".txt"
    ],
]


@pytest.mark.parametrize("symbolic_file_paths", test_failure_data)
def test_failure(symbolic_file_paths):
    with pytest.raises((ValueError, TypeError)):
        symbolic_file_paths_checker(symbolic_file_paths,
                                    valid_extensions=valid_extensions)


test_success_data = [["/etc/blah" + v] for v in valid_extensions]


@pytest.mark.parametrize("symbolic_file_paths", test_success_data)
def test_success(symbolic_file_paths):
    assert symbolic_file_paths_checker(symbolic_file_paths,
                                       valid_extensions=valid_extensions) is None
