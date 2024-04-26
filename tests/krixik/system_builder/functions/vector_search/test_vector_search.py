from tests.krixik.system_builder.functions.vector_search.utilities.setup import load_pipeline
from tests.utilities.dynamodb_interactions import check_meter
import uuid
import pytest


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline):
    """vector search failure when no query given"""
    with pytest.raises(
        ValueError, match=r".*query is empty - please enter a query\.*"
    ):
        pipeline.vector_search()


def test_2(pipeline):
    """vector search failure when no args given"""
    with pytest.raises(
        ValueError, match=r".*please provide at least one query argument\.*"
    ):
        pipeline.vector_search(query="hello world")


def test_3(pipeline, subtests):
    """vector_search succeeds with sort_order ascending, and check on created_at order"""
    with subtests.test(msg="main"):
        results = pipeline.vector_search(
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
    """vector_search succeeds with sort_order descending, and check on created_at order"""
    with subtests.test(msg="main-2"):
        results = pipeline.vector_search(
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
    """test vector_search with sort_order = global"""
    results = pipeline.vector_search(
        query="hello world",
        symbolic_directory_paths=["/*"],
        sort_order="global",
        max_files=10,
        k=1,
    )
    assert results["status_code"] == 200
    items = results["items"]
    no_search_results_count = 0
    for item in items:
        if "search_results" not in item:
            no_search_results_count += 1
    assert no_search_results_count == len(items)
    
    
def test_6(pipeline, subtests):
    """success with vector_search returning 200 code to dne input args"""
    query = "hello world"

    with subtests.test(msg="non extant symbolic_directory_path"):
        # non extant file_name
        results = pipeline.vector_search(
            query=query, file_names=["a file that does not exist.txt"]
        )
        assert results["status_code"] == 200
        assert len(results["items"]) == 0

    with subtests.test(msg="meter-1"):
        check_meter(results, single_record=False)

    with subtests.test(msg="non extant symbolic_file_path"):
        # non extant symbolic_directory_path
        results = pipeline.vector_search(
            query=query, symbolic_directory_paths=["/a/proper/file/path/to/nowwhere"]
        )
        assert results["status_code"] == 200

    with subtests.test(msg="meter-2"):
        check_meter(results, single_record=False)

    with subtests.test(msg="non extant symbolic_file_path"):
        # non extant symbolic_file_path
        results = pipeline.vector_search(
            query=query,
            symbolic_file_paths=[
                "/a/proper/file/path/to/nowwhere/a file that does not exist.txt"
            ],
        )
        assert results["status_code"] == 200
        assert len(results["items"]) == 0

    with subtests.test(msg="meter-3"):
        check_meter(results, single_record=False)

    with subtests.test(msg="non extant file_id"):
        # non extant file_id
        fake_file_id = str(uuid.uuid4())
        results = pipeline.vector_search(query=query, file_ids=[fake_file_id])
        assert results["status_code"] == 200
        assert len(results["items"]) == 0

    with subtests.test(msg="meter-4"):
        check_meter(results, single_record=False)


def test_7(pipeline):
    """successful vector search using file_name input arg"""
    query = "What is the foundation of business"

    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    test_file_name = all_items["items"][0]["file_name"]

    results = pipeline.vector_search(query=query, file_names=[test_file_name])
    assert results["status_code"] == 200


def test_8(pipeline):
    """successful vector search using symbolic_directory_path input arg"""
    query = "What is the foundation of business"

    # get first symbolic_directory_path from all_items
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    test_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

    results = pipeline.vector_search(
        query=query, symbolic_directory_paths=[test_symbolic_directory_path]
    )
    assert results["status_code"] == 200


def test_9(pipeline):
    """successful vector search using symbolic_file_path input arg"""
    query = "What is the foundation of business"

    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    test_file_name = all_items["items"][0]["file_name"]
    test_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
    test_symbolic_file_path = test_symbolic_directory_path + "/" + test_file_name

    results = pipeline.vector_search(
        query=query, symbolic_file_paths=[test_symbolic_file_path]
    )
    assert results["status_code"] == 200


def test_10(pipeline):
    """successful vector search using symbolic_directory_path stump input arg"""
    query = "What is the foundation of business"
    test_symbolic_directory_path_stump = "/home/*"

    results = pipeline.vector_search(
        query=query, symbolic_directory_paths=[test_symbolic_directory_path_stump]
    )
    assert results["status_code"] == 200
    
    
def test_11(pipeline):
    """successful vector search using mixed input arg"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    assert len(all_items["items"]) >= 1

    # get first item file_name and second file_id
    file_name = all_items["items"][0]["file_name"]
    file_id = all_items["items"][1]["file_id"]

    # run specific query
    results = pipeline.vector_search(
        query="hello world", file_ids=[file_id], file_names=[file_name]
    )

    # assert results
    assert len(results["items"]) >= 1

    # get first file_name and second symbolic_directory_path
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    file_name = all_items["items"][0]["file_name"]
    symbolic_directory_path = all_items["items"][1]["symbolic_directory_path"]

    # run specific list
    results = pipeline.vector_search(
        query="hello world",
        file_names=[file_name],
        symbolic_directory_paths=[symbolic_directory_path],
    )

    # assert results
    assert len(results["items"]) >= 1

    # run specific list
    results = pipeline.vector_search(
        query="hello world",
        file_ids=[file_id],
        symbolic_directory_paths=[symbolic_directory_path],
    )

    # assert results
    assert len(results["items"]) >= 1


def test_12(pipeline):
    """success with vector search using multiple file_ids"""
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
    query_results = pipeline.vector_search(
        query="hello world", file_ids=file_ids[:2]
    )

    # assert result contains error message
    assert query_results["status_code"] == 200 or query_results["status_code"] == 400


def test_13(pipeline):
    """success with vector search using multiple file_names"""
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

    # vector_search for first file_id and second file_name
    query_results = pipeline.vector_search(
        query="hello world", file_names=file_names[:2]
    )

    # assert result contains error message
    assert query_results["status_code"] == 200 or query_results["status_code"] == 400


def test_14(pipeline):
    """success with vector search using multiple symbolic_directory_paths"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # collect all symbolic_directory_paths
    symbolic_directory_paths = []
    for item in all_items["items"]:
        symbolic_directory_path = item["symbolic_directory_path"]
        symbolic_directory_paths.append(symbolic_directory_path)

    # get unique set
    symbolic_directory_paths = list(set(symbolic_directory_paths))

    # query for first file_id and second file_name
    query_results = pipeline.vector_search(
        query="hello world", symbolic_directory_paths=symbolic_directory_paths
    )

    # assert result contains error message
    assert query_results["status_code"] == 200


def test_15(pipeline):
    """success with vector search using multiple symbolic_directory_path stumps"""
    symbolic_directory_paths = ["/etc/*", "/my/*", "/home/*"]

    query_results = pipeline.vector_search(
        query="hello world", symbolic_directory_paths=symbolic_directory_paths
    )
    assert query_results["status_code"] == 200


def test_16(pipeline):
    """success with vector search using file_name previx"""
    query_results = pipeline.vector_search(query="hello world", file_names=["my*"])
    assert query_results["status_code"] == 200
    
    
def test_17(pipeline):
    """success with vector and keyword search using file_name suffix"""
    query_results = pipeline.vector_search(
        query="hello world", file_names=["*.txt"]
    )
    assert query_results["status_code"] == 200


def test_18(pipeline):
    """success with vector and keyword search using file_name substring"""
    query_results = pipeline.vector_search(
        query="hello world", file_names=["*life*"]
    )

    # assert result contains error message
    assert query_results["status_code"] == 200


def test_19(pipeline):
    """success with vector search using created_at_end"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # get listed item
    item = all_items["items"][0]
    item_id = item["file_id"]
    item_created_at = item["created_at"]
    item_last_updated = item["last_updated"]

    # try searching and recovering this file by created_at_end
    results = pipeline.vector_search(
        query="hello world", created_at_end=item_created_at
    )

    # collect all items
    result_items = results["items"]

    # collect all file_ids
    item_ids = [item["file_id"] for item in result_items]

    # assert that the file_id is in the listed_item_ids
    assert item_id in item_ids
    
    # try searching and recovering this file by last_updated_end
    results = pipeline.vector_search(
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
def test_20(pipeline, file_tags, expected_output):
    """success with keyword search using file_tags stump"""
    results = pipeline.vector_search(query="hello world", file_tags=file_tags)
    assert results["status_code"] == expected_output

    if file_tags == [{"book_category": "*"}]:
        assert len(results["items"]) > 1
        
        
def test_21(pipeline):
    """consistency of vector_search results from query k and k+1 over the same query and files"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # construct a test symbolic_file_path from the first item in all_items
    test_file_name = all_items["items"][0]["file_name"]
    test_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
    symbolic_file_path = test_symbolic_directory_path + "/" + test_file_name

    # define k_bar
    k_bar = 5
    query = "what is the foundation of business"
    first_query_results = pipeline.vector_search(
        query=query, symbolic_file_paths=[symbolic_file_path], k=k_bar
    )["items"][0]["search_results"][:k_bar]

    second_query_results = pipeline.vector_search(
        query=query, symbolic_file_paths=[symbolic_file_path], k=k_bar + 1
    )["items"][0]["search_results"][:k_bar]

    assert first_query_results == second_query_results

    # define k_bar
    k_bar = 5
    query = "real knowledge comes from work"
    first_query_results = pipeline.vector_search(
        query=query, symbolic_file_paths=[symbolic_file_path], k=k_bar
    )["items"][0]["search_results"][:k_bar]

    second_query_results = pipeline.vector_search(
        query=query, symbolic_file_paths=[symbolic_file_path], k=k_bar + 1
    )["items"][0]["search_results"][:k_bar]

    assert first_query_results == second_query_results
    

def test_22(pipeline):
    """consistency of results when using local sorting - all files should return the same number of results"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    # list all files - collect file_ids
    list_file_ids = [v["file_id"] for v in all_items["items"]]

    # search for hello world in all files
    k = 5
    search_results = pipeline.vector_search(
        query="hello world", file_ids=list_file_ids, k=k
    )

    # filter down to just results
    just_results = [v["search_results"] for v in search_results["items"]]

    # measure length of each result
    just_result_lengths = [len(v) for v in just_results]

    # assert length of just_result_lengths is greater than 1
    assert len(just_result_lengths) > 1

    # assert that just_result_lengths has all equal numbers
    assert all([v == k for v in just_result_lengths])


def test_23(pipeline):
    """alignment of file_id returns of list and query with same symbolic_directory_path stump"""
    def vector_search(symbolic_directory_path: str):
        output = pipeline.vector_search(
            query="hello world", symbolic_directory_paths=[symbolic_directory_path]
        )
        items = output["items"]
        warnings = output["warnings"]
        file_ids = set([item["file_id"] for item in items])
        return file_ids

    # list and query
    all_items = pipeline.list(symbolic_directory_paths=["/*"])

    symbolic_directory_path = "/*"
    file_ids_vector = set(
        [
            item["file_id"]
            for item in all_items["items"]
        ]
    )

    file_ids_vector_search = vector_search(symbolic_directory_path)

    # compare sets of file_ids
    assert file_ids_vector == file_ids_vector_search


test_data = [
    ({"chunk_size": 10, "overlap_size": 3}, 10),
    ({"chunk_size": 7, "overlap_size": 3}, 7),
]

    
def test_24(pipeline):
    """Ordinal checks of vector_search"""
    file_output_data = pipeline.vector_search(
        symbolic_directory_paths=[f"/*"], query="hello world", max_files=1, k=5
    )
    search_results = file_output_data["items"][0]["search_results"]
    snippets = [v["snippet"] for v in search_results]
    distances = [v["distance"] for v in search_results]

    # assert snippets are unique
    assert len(snippets) == len(set(snippets))

    # assert distances are in ascending order
    assert distances == sorted(distances)
    
    
def test_25(pipeline):
    """failure of both vector search when no query provided"""
    with pytest.raises(ValueError, match=r".*query is empty\.*"):
        pipeline.vector_search(
            symbolic_directory_paths=["/*"], sort_order="ascending", max_files=10
        )


def test_26(pipeline):
    """failure of both vector search when no query args provided"""
    with pytest.raises(
        ValueError, match=r".*please provide at least one query argument\.*"
    ):
        pipeline.vector_search(query="hello world")
        
        
def test_27(pipeline):
    """search successes with valid mixed arguments - one fake"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    query = "hello world"

    # dne file_name
    file_name = all_items["items"][0]["file_name"]
    file_id = all_items["items"][0]["file_id"]
    symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

    fake_file_name = "not a real file name.txt"
    results = pipeline.vector_search(
        query=query, file_ids=[file_id], file_names=[fake_file_name]
    )
    assert results["status_code"] == 200
    assert len(results["items"]) == 1
    warnings = results["warnings"]
    dne_file_name = list(warnings[0].values())[0][0]["file_names"][0]
    assert dne_file_name == fake_file_name

    # dne symbolic_directory_path
    fake_symbolic_directory_path = "/oh/hi/there"
    results = pipeline.vector_search(
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
    results = pipeline.vector_search(
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


def test_28(pipeline):
    """success with vector and keyword search using created_at_end other query args"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])
    first_item = all_items["items"][0]
    item_created_at = first_item["created_at"]

    # try searching and recovering this file by created_at_end
    result = pipeline.vector_search(
        query="hello world",
        symbolic_directory_paths=["/*"],
        created_at_end=item_created_at,
    )

    # collect all items
    assert result["status_code"] == 200


def test_29(pipeline):
    """ vector success with duplicate file_ids"""
    all_items = pipeline.list(symbolic_directory_paths=["/*"])["items"]
    file_ids = [item["file_id"] for item in all_items]
    listing_file_ids = [file_ids[0], file_ids[0], file_ids[1]]

    # vector search
    results = pipeline.vector_search(
        query="hello", file_ids=listing_file_ids, verbose=False
    )
    assert results["status_code"] == 200


def test_30(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0