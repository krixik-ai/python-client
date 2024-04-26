from tests.utilities.dynamodb_interactions import check_meter
import pytest
from tests.krixik.system_builder.functions.show_tree.utilities.setup import load_pipeline


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()



def test_2(pipeline, subtests):
    """successful usage of tree - including symbolic_directory_path and max_files"""
    with subtests.test(msg="main-1"):
        results = pipeline.show_tree(symbolic_directory_path="/*")
        assert results["status_code"] == 200

    with subtests.test(msg="meter-1"):
        check_meter(results, single_record=False)

    with subtests.test(msg="main-2"):
        results = pipeline.show_tree(symbolic_directory_path="/*", max_files=1)
        assert results["status_code"] == 200

    with subtests.test(msg="meter-2"):
        check_meter(results, single_record=False)
        
    
def test_3(pipeline):
    """check using list that all symbolic_directory_paths are valid and that no inter-pipeline leaking is happening"""
    # show_tree at root stump and collect all symbolic_directory_paths
    tree_output_data = pipeline.show_tree(
        symbolic_directory_path="/*", verbose=False
    )
    symbolic_file_paths = tree_output_data["items"]

    # list all symbolic_directory_paths
    list_output_data = pipeline.list(symbolic_file_paths=symbolic_file_paths)
    list_items = list_output_data["items"]

    # confirm there are a at least as many list_items as there were tree symbolic_directory_paths
    assert len(list_items) == len(symbolic_file_paths)

    # confirm that each item in list_items has the correct pipeline
    for item in list_items:
        assert item["pipeline"] == pipeline.pipeline


def test_4(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0