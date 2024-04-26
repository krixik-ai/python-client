from krixik.utilities.validators.system.base.symbolic_path_splitter import symbolic_path_splitter
import pytest


failure_data = [
    ("/my.mp4", ("", "my.mp4")),
    ("/a/pizza/good.txt", ("/a/pizza", "/good.txt"))
]

@pytest.mark.parametrize("failure_data", failure_data)
def test_1(failure_data):
    """failure tests for symbolic_file_path splitter """
    symbolic_file_name = failure_data[0]
    response = failure_data[1]
    symbolic_directory_path, file_name = symbolic_path_splitter(symbolic_file_name)
    assert symbolic_directory_path != response[0] or file_name != response[1]


success_data = [
    ("/my.mp4", ("/", "my.mp4")),
    ("/a/pizza/good.txt", ("/a/pizza", "good.txt"))
]

@pytest.mark.parametrize("success_data", success_data)
def test_2(success_data):
    """success tests for symbolic_file_path splitter """
    symbolic_file_name = success_data[0]
    response = success_data[1]
    symbolic_directory_path, file_name = symbolic_path_splitter(symbolic_file_name)
    assert symbolic_directory_path == response[0] and file_name == response[1]
