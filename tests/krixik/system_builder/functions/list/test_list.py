from tests.krixik.system_builder.functions.list.utilities.setup import load_pipeline
from tests.utilities.dynamodb_interactions import check_meter
import pytest
import uuid


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline):
    """list failure when no query arguments are given"""
    with pytest.raises(
        ValueError, match=r".*please provide at least one query argument\.*"
    ):
        pipeline.list()


def test_2(pipeline, subtests):
    """ list all successfully and check meter """
    results = pipeline.list(symbolic_directory_paths=["/*"])

    with subtests.test(msg="meter-1"):
        val = check_meter(results)
        assert val is True
        
    file_id = results["items"][1]["file_id"]
    file_name = results["items"][0]["file_name"]
    symbolic_directory_path = results["items"][1]["symbolic_directory_path"]
    first_file_tags = results["items"][0]["file_tags"]

    with subtests.test(msg="file_id"):
        results = pipeline.list(file_ids=[file_id])
        assert len(results["items"]) == 1
        assert results["items"][0]["pipeline"] == pipeline.pipeline
        
    with subtests.test(msg="meter-2"):
        val = check_meter(results)
        assert val is True

    with subtests.test(msg="file_name"):
        results = pipeline.list(file_names=[file_name])
        assert len(results["items"]) == 1
        assert results["items"][0]["pipeline"] == pipeline.pipeline
        
    with subtests.test(msg="meter-3"):
        val = check_meter(results)
        assert val is True
        
    with subtests.test(msg="symbolic_directory_path"):
        results = pipeline.list(symbolic_directory_paths=[symbolic_directory_path])
        assert len(results["items"]) >= 1
        
        pipeline_results = [v["pipeline"] for v in results["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])
        
    with subtests.test(msg="meter-4"):
        val = check_meter(results)
        assert val is True

    with subtests.test(msg="file_tags"):
        results = pipeline.list(file_tags=first_file_tags)
        assert len(results["items"]) >= 1
        
        pipeline_results = [v["pipeline"] for v in results["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])
        
    with subtests.test(msg="meter-5"):
        val = check_meter(results)
        assert val is True


def test_3(pipeline, subtests):
    """list successes with valid mixed arguments"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # get first item file_name and second file_id
    file_name = all_items["items"][0]["file_name"]
    file_id = all_items["items"][1]["file_id"]

    with subtests.test(msg="main-1"):
        results = pipeline.list(file_ids=[file_id], file_names=[file_name])
        assert len(results["items"]) == 2
        pipeline_results = [v["pipeline"] for v in results["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])

    with subtests.test(msg="meter-1"):
        val = check_meter(results)
        assert val is True

    # get first file_name and second symbolic_directory_path
    file_name = all_items["items"][0]["file_name"]
    symbolic_directory_path = all_items["items"][1]["symbolic_directory_path"]

    with subtests.test(msg="main-2"):
        results = pipeline.list(
            file_names=[file_name], symbolic_directory_paths=[symbolic_directory_path]
        )
        assert len(results["items"]) >= 2
        pipeline_results = [v["pipeline"] for v in results["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])

    with subtests.test(msg="meter-2"):
        val = check_meter(results)
        assert val is True

    # get first file_id and second symbolic_directory_path
    file_id = all_items["items"][0]["file_id"]
    symbolic_directory_path = all_items["items"][1]["symbolic_directory_path"]

    with subtests.test(msg="main-3"):
        results = pipeline.list(
            file_ids=[file_id], symbolic_directory_paths=[symbolic_directory_path]
        )
        assert len(results["items"]) >= 2
        pipeline_results = [v["pipeline"] for v in results["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])

    with subtests.test(msg="meter-3"):
        val = check_meter(results)
        assert val is True


def test_4(pipeline, subtests):
    """list success using symbolic_file_path"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    first_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
    first_file_name = all_items["items"][0]["file_name"]
    test_symbolic_file_path = first_symbolic_directory_path + "/" + first_file_name

    with subtests.test(msg="main"):
        results = pipeline.list(symbolic_file_paths=[test_symbolic_file_path])
        assert len(results["items"]) == 1
        pipeline_results = [v["pipeline"] for v in results["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])

    with subtests.test(msg="meter"):
        val = check_meter(results)
        assert val is True


test_data = [
    "*.json",
    "*krixik*",
]


@pytest.mark.parametrize("file_name", test_data)
def test_5(pipeline, file_name):
    """list success using file_name suffix, prefix, and substring"""
    results = pipeline.list(file_names=[file_name])
    assert len(results["items"]) >= 1

    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])


def test_6(pipeline, subtests):
    """list succeeds when listing via bookends - created_at_start, created_at_end, last_updated_start, last_updated_end"""

    # list a file
    list_result = pipeline.list(symbolic_directory_paths=["/*"], max_files=1)

    # get listed item
    item = list_result["items"][0]
    item_id = item["file_id"]
    item_created_at = item["created_at"]
    item_last_updated = item["last_updated"]

    with subtests.test(msg="created_at_start"):
        # try listing and recovering this file by created_at_start
        list_result = pipeline.list(created_at_start=item_created_at)

        # collect all listed items
        listed_items = list_result["items"]

        # collect all file_ids
        listed_item_ids = [item["file_id"] for item in listed_items]

        # assert that the file_id is in the listed_item_ids
        assert item_id in listed_item_ids
        pipeline_results = [v["pipeline"] for v in list_result["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])

    with subtests.test(msg="meter-1"):
        val = check_meter(list_result)
        assert val is True

    with subtests.test(msg="created_at_end"):
        # try listing and recovering this file by created_at_end
        list_result = pipeline.list(created_at_end=item_created_at)
        pipeline_results = [v["pipeline"] for v in list_result["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])
        
        # collect all listed items
        listed_items = list_result["items"]

        # collect all file_ids
        listed_item_ids = [item["file_id"] for item in listed_items]

        # assert that the file_id is in the listed_item_ids
        assert item_id in listed_item_ids

    with subtests.test(msg="meter-2"):
        val = check_meter(list_result)
        assert val is True

    with subtests.test(msg="last_updated_start"):
        # try listing and recovering this file by item_last_updated
        list_result = pipeline.list(last_updated_start=item_last_updated)
        pipeline_results = [v["pipeline"] for v in list_result["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])

        # collect all listed items
        listed_items = list_result["items"]

        # collect all file_ids
        listed_item_ids = [item["file_id"] for item in listed_items]

        # assert that the file_id is in the listed_item_ids
        assert item_id in listed_item_ids

    with subtests.test(msg="meter-3"):
        val = check_meter(list_result)
        assert val is True

    with subtests.test(msg="last_updated_end"):
        # try listing and recovering this file by item_last_updated
        list_result = pipeline.list(last_updated_end=item_last_updated)
        pipeline_results = [v["pipeline"] for v in list_result["items"]]
        assert all([v == pipeline.pipeline for v in pipeline_results])
        
        # collect all listed items
        listed_items = list_result["items"]

        # collect all file_ids
        listed_item_ids = [item["file_id"] for item in listed_items]

        # assert that the file_id is in the listed_item_ids
        assert item_id in listed_item_ids

    with subtests.test(msg="meter-4"):
        val = check_meter(list_result)
        assert val is True


def test_7(pipeline):
    """list succeeds when sort_order is ascending / descending"""
    results = pipeline.list(
        symbolic_directory_paths=["/*"], sort_order="ascending"
    )
    assert results["status_code"] == 200

    items = results["items"]
    created_ats = [item["created_at"] for item in items]
    assert sorted(created_ats) == created_ats
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])

    results = pipeline.list(
        symbolic_directory_paths=["/*"], sort_order="descending"
    )
    assert results["status_code"] == 200

    items = results["items"]
    created_ats = [item["created_at"] for item in items]
    assert sorted(created_ats, reverse=True) == created_ats
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    
    
def test_8(pipeline):
    """list succeeds with non extant query args - including file_id, file_name, symbolic_directory_path, symbolic_file_path"""
    # non extant file_id
    fake_file_id = str(uuid.uuid4())
    results = pipeline.list(file_ids=[fake_file_id])
    assert results["status_code"] == 200
    assert len(results["items"]) == 0

    warnings = results["warnings"]
    dne_file_id = list(warnings[0].values())[0][0]
    assert dne_file_id == fake_file_id

    # non extant file_name
    fake_file_name = "this file does not exist.json"
    results = pipeline.list(file_names=[fake_file_name])
    assert results["status_code"] == 200
    assert len(results["items"]) == 0

    warnings = results["warnings"]
    dne_file_name = list(warnings[0].values())[0][0]["file_names"][0]
    assert dne_file_name == fake_file_name

    # non extant symbolic_directory_path
    fake_directory_path = "/path/to/nowhere"
    results = pipeline.list(symbolic_directory_paths=[fake_directory_path])
    assert results["status_code"] == 200
    assert len(results["items"]) == 0

    warnings = results["warnings"]
    dne_directory_path = list(warnings[0].values())[0][0]["symbolic_directory_paths"][0]
    assert dne_directory_path == fake_directory_path

    # non extant fake_file_path
    fake_symbolic_file_path = "/path/to/nowhere/a file that does not exist.json"
    results = pipeline.list(symbolic_file_paths=[fake_symbolic_file_path])
    assert results["status_code"] == 200
    assert len(results["items"]) == 0

    warnings = results["warnings"]
    dne_symbolic_file_path = list(warnings[0].values())[0][0]["symbolic_file_paths"][0]
    assert dne_symbolic_file_path == fake_symbolic_file_path
    
    
def test_9(pipeline):
    """list succeeds with symbolic_directory_path stump"""
    stump_directory_path = "/home/*"
    results = pipeline.list(symbolic_directory_paths=[stump_directory_path])
    assert results["status_code"] == 200
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    

def test_10(pipeline):
    """list succeeds with max_files"""
    results = pipeline.list(symbolic_directory_paths=["/*"], max_files=1)
    assert results["status_code"] == 200
    assert len(results["items"]) == 1
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    

test_data = [
    ([{"century": "*"}], 200),
    ([{"book_category": "*"}], 200),
    ([{"book_category": "*"}, {"electronics": "*"}], 200),
    ([{"book_category": "*"}, {"electronics": "gameboy"}], 200),
]


@pytest.mark.parametrize("file_tags, expected", test_data)
def test_11(pipeline, file_tags, expected):
    """list succeeds with file_tag stumps"""
    results = pipeline.list(file_tags=file_tags, max_files=100)
    assert results["status_code"] == expected
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    
    # collect keys from file_tags
    keys = [list(tag.keys())[0] for tag in file_tags]

    # if century or book_category in keys, assert len of items is 2
    if "book_author" in keys or "book_category" in keys:
        assert len(results["items"]) == 2


def test_12(pipeline):
    """list succeeds with multiple file_ids, one fake file_id, verify fake_id is returned in warnings"""
    fake_file_id = str(uuid.uuid4())
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    file_ids = [item["file_id"] for item in all_items["items"]]
    file_ids.pop()
    file_ids.append(fake_file_id)
    results = pipeline.list(file_ids=file_ids)
    assert results["status_code"] == 200
    warnings = results["warnings"]
    dne_file_id = list(warnings[0].values())[0][0]
    assert dne_file_id == fake_file_id
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])


def test_13(pipeline):
    """list successes with valid mixed arguments - one fake"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # get first item file_name and second file_id
    file_name = all_items["items"][0]["file_name"]
    file_id = all_items["items"][0]["file_id"]
    symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

    # run specific list
    fake_file_name = "not a real file name.json"
    results = pipeline.list(file_ids=[file_id], file_names=[fake_file_name])
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    
    # assert results
    assert results["status_code"] == 200
    assert len(results["items"]) == 1
    warnings = results["warnings"]
    dne_file_name = list(warnings[0].values())[0][0]["file_names"][0]
    assert dne_file_name == fake_file_name

    # get first file_name and second symbolic_directory_path
    fake_symbolic_directory_path = "/oh/hi/there"

    # run specific list
    results = pipeline.list(
        file_names=[file_name], symbolic_directory_paths=[fake_symbolic_directory_path]
    )
    assert results["status_code"] == 200
    assert len(results["items"]) >= 1
    warnings = results["warnings"]
    dne_symbolic_directory_path = list(warnings[0].values())[0][0][
        "symbolic_directory_paths"
    ][0]
    assert dne_symbolic_directory_path == fake_symbolic_directory_path
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    
    # run specific list
    fake_file_id = str(uuid.uuid4())
    results = pipeline.list(
        file_ids=[fake_file_id], symbolic_directory_paths=[symbolic_directory_path]
    )
    assert results["status_code"] == 200
    assert len(results["items"]) >= 1
    warnings = results["warnings"]
    dne_file_id = list(warnings[0].values())[0][0]
    assert dne_file_id == fake_file_id
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    

def test_14(pipeline):
    """list success with duplicate file_ids"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])["items"]
    file_ids = [item["file_id"] for item in all_items]
    listing_file_ids = [file_ids[0], file_ids[0], file_ids[1]]
    results = pipeline.list(file_ids=listing_file_ids, verbose=False)
    assert results["status_code"] == 200
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    

def test_15(pipeline):
    """test for pipeline boundary crossing"""
    results = pipeline.list(symbolic_directory_paths=["/*"])
    assert results["status_code"] == 200
    pipeline_results = [v["pipeline"] for v in results["items"]]
    assert all([v == pipeline.pipeline for v in pipeline_results])
    

def test_16(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0