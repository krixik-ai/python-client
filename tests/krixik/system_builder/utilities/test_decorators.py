from krixik.system_builder.utilities.decorators import kwargs_checker, allowed_args_dict
import pytest

@kwargs_checker
def init(**kwargs):
    pass

@kwargs_checker
def delete(**kwargs):
    pass

@kwargs_checker
def list(**kwargs):
    pass

@kwargs_checker
def fetch_output(**kwargs):
    pass

@kwargs_checker
def update(**kwargs):
    pass

@kwargs_checker
def process(**kwargs):
    pass

@kwargs_checker
def show_tree(**kwargs):
    pass

@kwargs_checker
def process_status(**kwargs):
    pass

@kwargs_checker
def not_supported(**kwargs):
    pass


success_data = [
    (init , {"api_key": "123", "api_url": "https://www.google.com"}),
    (delete , {"file_id": "123"}),
    (list, {"file_ids": "123", "file_names": "good.txt", "symbolic_directory_paths": "/home", "symbolic_file_paths": "/home/good.txt", "file_tags": "good", "sort_order": "asc", "max_files": 10, "created_at_start": "2021-01-01", "created_at_end": "2021-01-01", "last_updated_start": "2021-01-01", "last_updated_end": "2021-01-01", "verbose": "True"}),
    (fetch_output, {"file_id": "123", "local_save_directory": "/home"}),
    (update, {"file_id": "123", "file_name": "good.txt", "symbolic_directory_path": "/home", "symbolic_file_path": "/home/good.txt", "file_tags": "good", "file_description": "good", "expire_time": "2021-01-01", "verbose": "True"}),
    (process, {"file_id": "123", "file_name": "good.txt", "symbolic_directory_path": "/home", "symbolic_file_path": "/home/good.txt", "local_file_path": "/home/good.txt", "file_tags": "good", "file_description": "good", "modules": "good", "expire_time": "2021-01-01", "verbose": "True", "wait_for_process": "True", "local_save_directory": "/home", "og_local_file_path": "/home/good.txt"}),
    (show_tree, {"symbolic_directory_path": "/home", "max_files": 10, "verbose": "True"}),
    (process_status, {"process_id": "123"}),
]


def test_0():
    """ assert that all functions in allowed_args_dict are covered in success_data """
    success_function_names = [func_data[0].__name__ for func_data in success_data]
    allowed_function_names = allowed_args_dict.keys()
    assert set(success_function_names) == set(allowed_function_names)


failure_data = [
    (init , {"ice cream ": "123", " api_url": "https://www.google.com"}),
    (delete , {"verbose": "True"}),
    (list, {"file_id": "123", "file_names": "good.txt"}),
    (list, {"file_name": "good.txt"}),
    (fetch_output, {"file_name": "123", "local_save_directory": "/home"}),
    (update, {"file_ids": "123", "file_name": "good.txt"}),
    (process, {"file_ids": "123", "file_name": "good.txt"}),
    (show_tree, {"symbolic_file_path": "/home", "max_files": 10}),
    (process_status, {"file_id": "123"}),
]

@pytest.mark.parametrize("failure_data", failure_data)
def test_1(failure_data):
    """failure tests for kwargs_checker """
    func_name = failure_data[0]
    kwargs = failure_data[1]
    with pytest.raises(TypeError, match=r".*unexpected keyword argument\.*"):
        func_name(**kwargs) 
        

def test_2():
    """ failure for wrapping unsupported function """
    with pytest.raises(ValueError, match=r".*function not supported.*"):
        not_supported()