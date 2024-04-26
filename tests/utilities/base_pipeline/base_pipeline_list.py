from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.decorators import capture_printed_output
import pytest
import uuid


def confirm_pipeline(items: list, target_pipeline: str):
    pipelines = [v["pipeline"] for v in items]
    assert all([v == target_pipeline for v in pipelines])


class BasePipelineList(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)
        self.test_data = []
        self.available_pipelines = []

    @capture_printed_output
    def list_print(self, **kwargs):
        self.list_all(**kwargs)

    def test_1(self):
        """failure to process due to bad init / not first initialized"""
        self.check_bad_init()

        # attempt to process
        with pytest.raises(ValueError, match=r".*you are not authenticated\.*"):
            self.list_all()

    def test_2(self):
        """list failure when no query arguments are given"""
        self.check_good_init()

        # attempt to process
        with pytest.raises(
            ValueError, match=r".*please provide at least one query argument\.*"
        ):
            self.base_pipeline.list()

    def test_3(self, subtests):
        """list successes with single valid arguments"""
        self.check_good_init()
        all_items = self.list_all()
        file_id = all_items["items"][1]["file_id"]
        file_name = all_items["items"][0]["file_name"]
        symbolic_directory_path = all_items["items"][1]["symbolic_directory_path"]
        first_file_tags = all_items["items"][0]["file_tags"]
        some_file_tags = [
            {"book_category": "nonfiction"},
            {"book_author": "ford"},
            {"book_title": "my_life_and_work"},
        ]

        with subtests.test(msg="main-1"):
            results = self.base_pipeline.list(file_ids=[file_id])
            assert len(results["items"]) == 1
            confirm_pipeline(results["items"], self.pipeline)

        with subtests.test(msg="meter-1"):
            check_meter(results, single_record=True)

        with subtests.test(msg="main-2"):
            results = self.base_pipeline.list(file_names=[file_name])
            assert len(results["items"]) == 1
            confirm_pipeline(results["items"], self.pipeline)

        with subtests.test(msg="meter-2"):
            check_meter(results, single_record=True)

        with subtests.test(msg="main-3"):
            results = self.base_pipeline.list(
                symbolic_directory_paths=[symbolic_directory_path]
            )
            assert len(results["items"]) >= 1
            confirm_pipeline(results["items"], self.pipeline)

        with subtests.test(msg="meter-3"):
            check_meter(results, single_record=True)

        with subtests.test(msg="main-4"):
            results = self.base_pipeline.list(file_tags=some_file_tags)
            assert len(results["items"]) >= 1
            confirm_pipeline(results["items"], self.pipeline)

        with subtests.test(msg="meter-4"):
            check_meter(results, single_record=True)

    def test_4(self):
        """list successes with valid mixed arguments"""
        self.check_good_init()

        all_items = self.list_all()

        # get first item file_name and second file_id
        file_name = all_items["items"][0]["file_name"]
        file_id = all_items["items"][1]["file_id"]

        # run specific list
        results = self.base_pipeline.list(file_ids=[file_id], file_names=[file_name])

        # assert results
        assert len(results["items"]) == 2
        confirm_pipeline(results["items"], self.pipeline)

        # get first file_name and second symbolic_directory_path
        file_name = all_items["items"][0]["file_name"]
        symbolic_directory_path = all_items["items"][1]["symbolic_directory_path"]

        # run specific list
        results = self.base_pipeline.list(
            file_names=[file_name], symbolic_directory_paths=[symbolic_directory_path]
        )

        # assert results
        assert len(results["items"]) >= 2
        confirm_pipeline(results["items"], self.pipeline)

        # run specific list
        file_id = all_items["items"][1]["file_id"]
        symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

        results = self.base_pipeline.list(
            file_ids=[file_id], symbolic_directory_paths=[symbolic_directory_path]
        )

        # assert results
        assert len(results["items"]) >= 2
        confirm_pipeline(results["items"], self.pipeline)

    def test_5(self):
        """list success using symbolic_file_path"""
        self.check_good_init()

        all_items = self.list_all()
        first_symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
        first_file_name = all_items["items"][0]["file_name"]
        test_symbolic_file_path = first_symbolic_directory_path + "/" + first_file_name
        results = self.base_pipeline.list(symbolic_file_paths=[test_symbolic_file_path])
        assert len(results["items"]) == 1
        confirm_pipeline(results["items"], self.pipeline)

    def test_6(self, file_name: str):
        """list success using file_name suffix, prefix, and substring"""
        self.check_good_init()

        results = self.base_pipeline.list(file_names=[file_name])
        assert len(results["items"]) >= 1
        confirm_pipeline(results["items"], self.pipeline)

    def test_7(self):
        """list succeeds when listing via bookends - created_at_start, created_at_end, last_updated_start, last_updated_end"""
        self.check_good_init()

        # list a file
        list_result = self.base_pipeline.list(
            symbolic_directory_paths=["/*"], max_files=1
        )

        # get listed item
        item = list_result["items"][0]
        item_id = item["file_id"]
        item_created_at = item["created_at"]
        item_last_updated = item["last_updated"]

        # try listing and recovering this file by created_at_end
        list_result = self.base_pipeline.list(created_at_end=item_created_at)

        # collect all listed items
        listed_items = list_result["items"]

        # collect all file_ids
        listed_item_ids = [item["file_id"] for item in listed_items]

        # assert that the file_id is in the listed_item_ids
        assert item_id in listed_item_ids
        confirm_pipeline(list_result["items"], self.pipeline)

        # try listing and recovering this file by item_last_updated
        list_result = self.base_pipeline.list(last_updated_end=item_last_updated)

        # collect all listed items
        listed_items = list_result["items"]

        # collect all file_ids
        listed_item_ids = [item["file_id"] for item in listed_items]

        # assert that the file_id is in the listed_item_ids
        assert item_id in listed_item_ids
        confirm_pipeline(list_result["items"], self.pipeline)

    def test_8(self):
        """list succeeds when sort_order is ascending"""
        self.check_good_init()

        results = self.base_pipeline.list(
            symbolic_directory_paths=["/*"], sort_order="ascending"
        )
        assert results["status_code"] == 200

        items = results["items"]
        created_ats = [item["created_at"] for item in items]
        assert sorted(created_ats) == created_ats
        confirm_pipeline(results["items"], self.pipeline)

    def test_9(self):
        """list succeeds when sort_order is descending"""
        self.check_good_init()

        results = self.base_pipeline.list(
            symbolic_directory_paths=["/*"], sort_order="descending"
        )
        assert results["status_code"] == 200

        items = results["items"]
        created_ats = [item["created_at"] for item in items]
        assert sorted(created_ats, reverse=True) == created_ats
        confirm_pipeline(results["items"], self.pipeline)

    def test_10(self, fake_file_name: str, fake_symbolic_file_path: str):
        """list succeeds with non extant query args - including file_id, file_name, symbolic_directory_path, symbolic_file_path"""
        self.check_good_init()

        # non extant file_id
        fake_file_id = str(uuid.uuid4())
        results = self.base_pipeline.list(file_ids=[fake_file_id])
        assert results["status_code"] == 200
        assert len(results["items"]) == 0
        warnings = results["warnings"]
        dne_file_id = list(warnings[0].values())[0][0]
        assert dne_file_id == fake_file_id

        # non extant file_name
        results = self.base_pipeline.list(file_names=[fake_file_name])
        assert results["status_code"] == 200
        assert len(results["items"]) == 0

        warnings = results["warnings"]
        dne_file_name = list(warnings[0].values())[0][0]["file_names"][0]
        assert dne_file_name == fake_file_name

        # non extant symbolic_directory_path
        fake_directory_path = "/path/to/nowhere"
        results = self.base_pipeline.list(
            symbolic_directory_paths=[fake_directory_path]
        )
        assert results["status_code"] == 200
        assert len(results["items"]) == 0

        warnings = results["warnings"]
        dne_directory_path = list(warnings[0].values())[0][0][
            "symbolic_directory_paths"
        ][0]
        assert dne_directory_path == fake_directory_path

        # non extant fake_file_path
        results = self.base_pipeline.list(symbolic_file_paths=[fake_symbolic_file_path])
        assert results["status_code"] == 200
        assert len(results["items"]) == 0

        warnings = results["warnings"]
        dne_symbolic_file_path = list(warnings[0].values())[0][0][
            "symbolic_file_paths"
        ][0]
        assert dne_symbolic_file_path == fake_symbolic_file_path

    def test_11(self):
        """list succeeds with symbolic_directory_path stump"""
        self.check_good_init()

        stump_directory_path = "/home/*"
        results = self.base_pipeline.list(
            symbolic_directory_paths=[stump_directory_path]
        )
        assert results["status_code"] == 200
        confirm_pipeline(results["items"], self.pipeline)

    def test_12(self):
        """list succeeds with max_files"""
        self.check_good_init()

        results = self.base_pipeline.list(symbolic_directory_paths=["/*"], max_files=1)
        assert results["status_code"] == 200
        assert len(results["items"]) == 1
        confirm_pipeline(results["items"], self.pipeline)

    test_data = [
        ([{"century": "*"}], 200),
        ([{"book_category": "*"}], 200),
        ([{"book_category": "*"}, {"electronics": "*"}], 200),
        ([{"book_category": "*"}, {"electronics": "gameboy"}], 200),
    ]

    @pytest.mark.parametrize("file_tags, expected", test_data)
    def test_13(self, file_tags, expected):
        """list succeeds with file_tags stump"""
        self.check_good_init()

        results = self.base_pipeline.list(file_tags=file_tags, max_files=10)
        assert results["status_code"] == expected
        if expected == 200:
            confirm_pipeline(results["items"], self.pipeline)

        # collect keys from file_tags
        keys = [list(tag.keys())[0] for tag in file_tags]

        # if century or book_category in keys, assert len of items is 2
        if "book_category" in keys:
            assert len(results["items"]) == 2, f"results: {results}"

    def test_14(self, file_name, expected_output):
        """list succeeds with all current embedding_options uploaded files"""
        self.check_good_init()

        file_names = [file_name]
        results = self.base_pipeline.list(file_names=file_names)
        assert results["status_code"] == expected_output
        confirm_pipeline(results["items"], self.pipeline)

    def test_15(self):
        """list succeeds with multiple file_ids, one fake file_id, verify fake_id is returned in warnings"""
        self.check_good_init()

        fake_file_id = str(uuid.uuid4())
        all_items = self.list_all()
        file_ids = [item["file_id"] for item in all_items["items"]]
        file_ids.pop()
        file_ids.append(fake_file_id)
        results = self.base_pipeline.list(file_ids=file_ids)
        assert results["status_code"] == 200
        confirm_pipeline(results["items"], self.pipeline)

        warnings = results["warnings"]
        dne_file_id = list(warnings[0].values())[0][0]
        assert dne_file_id == fake_file_id

    def test_16(self, fake_file_name):
        """list successes with valid mixed arguments - one fake"""
        self.check_good_init()

        all_items = self.list_all()

        # get first item file_name and second file_id
        file_name = all_items["items"][0]["file_name"]
        file_id = all_items["items"][0]["file_id"]
        symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]

        # run specific list
        results = self.base_pipeline.list(
            file_ids=[file_id], file_names=[fake_file_name]
        )
        confirm_pipeline(results["items"], self.pipeline)

        # assert results
        assert results["status_code"] == 200
        assert len(results["items"]) == 1
        warnings = results["warnings"]
        dne_file_name = list(warnings[0].values())[0][0]["file_names"][0]
        assert dne_file_name == fake_file_name

        # get first file_name and second symbolic_directory_path
        fake_symbolic_directory_path = "/oh/hi/there"

        # run specific list
        results = self.base_pipeline.list(
            file_names=[file_name],
            symbolic_directory_paths=[fake_symbolic_directory_path],
        )
        assert results["status_code"] == 200
        assert len(results["items"]) >= 1
        confirm_pipeline(results["items"], self.pipeline)

        warnings = results["warnings"]
        dne_symbolic_directory_path = list(warnings[0].values())[0][0][
            "symbolic_directory_paths"
        ][0]
        assert dne_symbolic_directory_path == fake_symbolic_directory_path

        # run specific list
        fake_file_id = str(uuid.uuid4())
        results = self.base_pipeline.list(
            file_ids=[fake_file_id], symbolic_directory_paths=[symbolic_directory_path]
        )
        assert results["status_code"] == 200
        assert len(results["items"]) >= 1
        confirm_pipeline(results["items"], self.pipeline)

        warnings = results["warnings"]
        dne_file_ids_warning = [
            v
            for v in warnings
            if "WARNING: the following file_ids were not found" in list(v.keys())[0]
        ][0]
        dne_file_id = list(dne_file_ids_warning.values())[0][0]
        assert dne_file_id == fake_file_id

    def test_17(self):
        """list success with verbose true"""
        self.check_good_init()

        result = self.list_print(verbose=True)

        assert "value of max_files not set by user" in result["printed_output"]

    def test_18(self):
        """list success with verbose false"""
        self.check_good_init()

        result = self.list_print(verbose=False)

        assert len(result["printed_output"]) == 0

    def test_19(self):
        """list success with duplicate file_ids"""
        self.check_good_init()

        all_items = self.list_all()["items"]
        file_ids = [item["file_id"] for item in all_items]
        listing_file_ids = [file_ids[0], file_ids[0], file_ids[1]]
        results = self.base_pipeline.list(file_ids=listing_file_ids, verbose=False)
        assert results["status_code"] == 200

    def test_20(self):
        """test for pipeline boundary crossing"""
        self.check_good_init()
        results = self.list_all()
        assert results["status_code"] == 200
        pipelines = [v["pipeline"] for v in results["items"]]
        assert all([v == self.pipeline for v in pipelines])
