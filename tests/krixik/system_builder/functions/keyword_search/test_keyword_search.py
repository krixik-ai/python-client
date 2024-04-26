from tests.krixik.system_builder.functions.keyword_search.utilities.setup import load_pipeline
from tests.utilities.dynamodb_interactions import check_meter
import pytest
import uuid


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline):
    """search failure when no query given"""
    with pytest.raises(
        ValueError, match=r".*query is empty - please enter a query\.*"
    ):
        pipeline.keyword_search()


def test_2(pipeline):
    """search failure when no args given"""
    with pytest.raises(
        ValueError, match=r".*please provide at least one query argument\.*"
    ):
        pipeline.keyword_search(query="hello world")
        
        
def test_3(pipeline, subtests):
    """keyword_search succeeds with sort_order ascending, and check on created_at order"""
    with subtests.test(msg="main"):
        results = pipeline.keyword_search(
            query="hello world",
            symbolic_directory_paths=["/*"],
            sort_order="ascending",
            max_files=10,
        )
        assert results["status_code"] == 200
        created_ats = [item["file_metadata"]["created_at"] for item in results["items"]]
        assert sorted(created_ats) == created_ats

    with subtests.test(msg="meter"):
        check_meter(results, single_record=False)


def test_4(pipeline, subtests):
    """keyword_search succeeds with sort_order descending, and check on created_at order"""
    with subtests.test(msg="main-2"):
        results = pipeline.keyword_search(
            query="hello world",
            symbolic_directory_paths=["/*"],
            sort_order="descending",
            max_files=10,
        )
        assert results["status_code"] == 200
        created_ats = [item["file_metadata"]["created_at"] for item in results["items"]]
        assert sorted(created_ats, reverse=True) == created_ats

    with subtests.test(msg="meter-2"):
        check_meter(results, single_record=False)
        

def test_5(pipeline):
    """success with keyword_search returning 200 code to dne input args"""
    query = "hello world"

    # non extant symbolic_directory_path
    results = pipeline.keyword_search(
        query=query, symbolic_directory_paths=["/a/proper/file/path/to/nowwhere"]
    )
    assert results["status_code"] == 200
    assert len(results["items"]) == 0

    # non extant symbolic_file_path
    results = pipeline.keyword_search(
        query=query,
        symbolic_file_paths=[
            "/a/proper/file/path/to/nowwhere/a file that does not exist.txt"
        ],
    )
    assert results["status_code"] == 200
    assert len(results["items"]) == 0

    # non extant file_id
    fake_file_id = str(uuid.uuid4())
    results = pipeline.keyword_search(query=query, file_ids=[fake_file_id])
    assert results["status_code"] == 200
    assert len(results["items"]) == 0


def test_6(pipeline):
    """successful keyword search using file_name input arg"""
    query = "What is the foundation of business"

    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    test_file_name = all_items["items"][0]["file_name"]

    results = pipeline.keyword_search(query=query, file_names=[test_file_name])
    assert results["status_code"] == 200


def test_7(pipeline):
    """successful keyword search using symbolic_directory_path input arg"""
    query = "What is the foundation of business"

    # get first symbolic_directory_path from all_items
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    test_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

    results = pipeline.keyword_search(
        query=query, symbolic_directory_paths=[test_symbolic_directory_path]
    )
    assert results["status_code"] == 200


def test_8(pipeline):
    """successful keyword search using symbolic_file_path input arg"""
    query = "What is the foundation of business"

    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    test_file_name = all_items["items"][0]["file_name"]
    test_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
    test_symbolic_file_path = test_symbolic_directory_path + "/" + test_file_name

    results = pipeline.keyword_search(
        query=query, symbolic_file_paths=[test_symbolic_file_path]
    )
    assert results["status_code"] == 200
    
    
def test_9(pipeline):
    """successful keyword search using symbolic_directory_path stump input arg"""
    query = "What is the foundation of business"
    test_symbolic_directory_path_stump = "/home/*"

    results = pipeline.keyword_search(
        query=query, symbolic_directory_paths=[test_symbolic_directory_path_stump]
    )
    assert results["status_code"] == 200
    
    
def test_10(pipeline):
    """successful keyword and vector search using mixed input arg"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    assert len(all_items["items"]) >= 1

    # get first item file_name and second file_id
    file_name = all_items["items"][0]["file_name"]
    file_id = all_items["items"][1]["file_id"]


    # run specific query
    results = pipeline.keyword_search(
        query="It was a bright cold day in April", file_ids=[file_id], file_names=[file_name]
    )

    # assert results
    assert len(results["items"]) >= 1

    # get first file_name and second symbolic_directory_path
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    file_name = all_items["items"][0]["file_name"]
    symbolic_directory_path = all_items["items"][1]["symbolic_directory_path"]

    # run specific list
    results = pipeline.keyword_search(
        query="hello world",
        file_names=[file_name],
        symbolic_directory_paths=[symbolic_directory_path],
    )

    # assert results
    assert len(results["items"]) >= 1

    # run specific list
    results = pipeline.keyword_search(
        query="hello world",
        file_ids=[file_id],
        symbolic_directory_paths=[symbolic_directory_path],
    )

    # assert results
    assert len(results["items"]) >= 1
    
    
def test_11(pipeline):
    """success with keyword search using multiple file_ids"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    file_ids = []
    for item in all_items["items"]:
        file_id = item["file_id"]
        file_ids.append(file_id)

    # get unique set
    file_ids = list(set(file_ids))

    # ensure more than one file exists
    assert len(file_ids) > 1

    # query for first file_id and second file_name
    query_results = pipeline.keyword_search(
        query="hello world", file_ids=file_ids[:2]
    )

    # assert result contains error message
    assert query_results["status_code"] == 200 or query_results["status_code"] == 400


def test_12(pipeline):
    """success with keyword and vector search using multiple file_names"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # collect all file_names
    file_names = []
    for item in all_items["items"]:
        file_name = item["file_name"]
        file_names.append(file_name)

    # get unique set
    file_names = list(set(file_names))

    # ensure more than one file exists
    assert len(file_names) > 1

    # keyword_search for first file_id and second file_name
    query_results = pipeline.keyword_search(
        query="hello world", file_names=file_names[:2]
    )

    # assert result contains error message
    assert query_results["status_code"] == 200 or query_results["status_code"] == 400


def test_13(pipeline):
    """success with keyword search using multiple symbolic_directory_paths"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # collect all symbolic_directory_paths
    symbolic_directory_paths = []
    for item in all_items["items"]:
        symbolic_directory_path = item["symbolic_directory_path"]
        symbolic_directory_paths.append(symbolic_directory_path)

    # get unique set
    symbolic_directory_paths = list(set(symbolic_directory_paths))

    # query for first file_id and second file_name
    query_results = pipeline.keyword_search(
        query="hello world", symbolic_directory_paths=symbolic_directory_paths
    )

    # assert result contains error message
    assert query_results["status_code"] == 200


def test_14(pipeline):
    """success with keyword and vector search using multiple symbolic_directory_path stumps"""
    symbolic_directory_paths = ["/etc/*", "/my/*", "/home/*"]

    query_results = pipeline.keyword_search(
        query="hello world", symbolic_directory_paths=symbolic_directory_paths
    )
    assert query_results["status_code"] == 200
    
    
def test_15(pipeline):
    """success with keyword and vector search using file_name previx"""
    query_results = pipeline.keyword_search(
        query="hello world", file_names=["my*"]
    )
    assert query_results["status_code"] == 200
    

def test_16(pipeline):
    """success with vector and keyword search using file_name suffix"""
    query_results = pipeline.keyword_search(
        query="hello world", file_names=["*.txt"]
    )
    assert query_results["status_code"] == 200
    

def test_17(pipeline):
    """success with vector and keyword search using file_name substring"""
    # keyword search by suffix
    query_results = pipeline.keyword_search(
        query="hello world", file_names=["*life*"]
    )

    # assert result contains error message
    assert query_results["status_code"] == 200
    
    
def test_18(pipeline):
    """success with vector and keyword search using created_at_end"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # get listed item
    item = all_items["items"][0]
    item_id = item["file_id"]
    item_created_at = item["created_at"]
    item_last_updated = item["last_updated"]

    # try searching and recovering this file by created_at_end
    results = pipeline.keyword_search(
        query="It was a bright cold day in April watched keenly and closely by intelligences",
        created_at_end=item_created_at
    )

    # collect all items
    result_items = results["items"]

    # collect all file_ids
    item_ids = [item["file_id"] for item in result_items]

    # assert that the file_id is in the listed_item_ids
    assert item_id in item_ids

    # try searching and recovering this file by last_updated_end
    results = pipeline.keyword_search(
        query="hello world", last_updated_end=item_last_updated
    )

    # collect all items
    result_items = results["items"]

    # collect all file_ids
    item_ids = [item["file_id"] for item in result_items]

    # assert that the file_id is in the listed_item_ids
    assert item_id in item_ids


test_data = [
    ([{"book_category": "*"}], 200),
    ([{"book_category": "nonfiction"}], 200),
]


@pytest.mark.parametrize("file_tags, expected_output", test_data)
def test_19(pipeline, file_tags, expected_output):
    """success with keyword search using file_tags stump"""
    results = pipeline.keyword_search(query="hello world", file_tags=file_tags)
    assert results["status_code"] == expected_output

    if file_tags == [{"book_category": "*"}]:
        assert len(results["items"]) > 1


def test_20(pipeline):
    """alignment of file_id returns of list and query with same symbolic_directory_path stump"""
    def keyword_search(symbolic_directory_path: str):
        output = pipeline.keyword_search(
            query="hello world", symbolic_directory_paths=[symbolic_directory_path]
        )
        items = output["items"]
        warnings = output["warnings"]

        # collect file_ids from WARNING: the following file_ids returned no results for the given query warning
        file_ids = [item["file_id"] for item in items]
        warning_file_ids = []
        for warning in warnings:
            if isinstance(warning, dict):
                if (
                    "WARNING: the following file_ids returned no results for the given query"
                    in list(warning.keys())[0]
                ):
                    warning_file_ids.extend(list(warning.values())[0])

        file_ids += warning_file_ids

        return set(file_ids)

    # list and query
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    symbolic_directory_path = "/*"
    file_ids_keyword = set(
        [
            item["file_id"]
            for item in all_items["items"]
        ]
    )
    file_ids_keyword_search = keyword_search(symbolic_directory_path)

    # compare sets of file_ids
    assert file_ids_keyword == file_ids_keyword_search
    
    
def test_21(pipeline):
    """failure of both keyword and vector search when no query provided"""
    with pytest.raises(ValueError, match=r".*query is empty\.*"):
        pipeline.keyword_search(
            symbolic_directory_paths=["/*"], sort_order="ascending", max_files=10
        )


def test_22(pipeline):
    """failure of both keyword and vector search when no query args provided"""
    with pytest.raises(
        ValueError, match=r".*please provide at least one query argument\.*"
    ):
        pipeline.keyword_search(query="hello world")


def test_23(pipeline):
    """search successes with valid mixed arguments - one fake"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    query = "hello world"

    # dne file_name
    file_name = all_items["items"][0]["file_name"]
    file_id = all_items["items"][0]["file_id"]
    symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

    fake_file_name = "not a real file name.txt"
    results = pipeline.keyword_search(
        query=query, file_ids=[file_id], file_names=[fake_file_name]
    )
    assert results["status_code"] == 200
    assert len(results["items"]) == 1
    warnings = results["warnings"]
    dne_file_name = list(warnings[0].values())[0][0]["file_names"][0]
    assert dne_file_name == fake_file_name

    # dne symbolic_directory_path
    fake_symbolic_directory_path = "/oh/hi/there"
    results = pipeline.keyword_search(
        query=query,
        file_names=[file_name],
        symbolic_directory_paths=[fake_symbolic_directory_path],
    )
    assert results["status_code"] == 200
    assert len(results["items"]) >= 1
    warnings = results["warnings"]
    dne_symbolic_directory_path = list(warnings[0].values())[0][0][
        "symbolic_directory_paths"
    ][0]
    assert dne_symbolic_directory_path == fake_symbolic_directory_path

    # dne file_id
    fake_file_id = str(uuid.uuid4())
    results = pipeline.keyword_search(
        query=query,
        file_ids=[fake_file_id],
        symbolic_directory_paths=[symbolic_directory_path],
    )

    assert results["status_code"] == 200
    assert len(results["items"]) >= 1
    warnings = results["warnings"]

    dne_warning = [
        v
        for v in warnings
        if "WARNING: the following file_ids were not found" in list(v.keys())[0]
    ]
    dne_file_ids = [list(v.values())[0] for v in dne_warning][0]
    assert fake_file_id in dne_file_ids


def test_24(pipeline):
    """success with vector and keyword search using created_at_end other query args"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    first_item = all_items["items"][0]
    item_created_at = first_item["created_at"]

    # try searching and recovering this file by created_at_end
    result = pipeline.keyword_search(
        query="hello world",
        symbolic_directory_paths=["/*"],
        created_at_end=item_created_at,
    )

    # collect all items
    assert result["status_code"] == 200


def test_25(pipeline):
    """keyword and vector success with duplicate file_ids"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    file_ids = [item["file_id"] for item in all_items["items"]]
    listing_file_ids = [file_ids[0], file_ids[0], file_ids[1]]

    # keyword search
    results = pipeline.keyword_search(
        query="It was a bright cold day in April watched keenly and closely by intelligences", file_ids=listing_file_ids, verbose=False
    )
    assert results["status_code"] == 200


def test_26(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0