from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.decorators import capture_printed_output
import pytest


class BasePipelineTree(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)
        self.test_data = []
        self.available_pipelines = []

    @capture_printed_output
    def show_print(self, **kwargs):
        self.base_pipeline.show_tree(**kwargs)

    def test_1(self):
        """failure to process due to bad init / not first initialized"""
        self.check_bad_init()

        # attempt to process
        with pytest.raises(ValueError, match=r".*you are not authenticated\.*"):
            self.base_pipeline.show_tree(symbolic_directory_path="/*")

    def test_2(self):
        """failure due to no input arg"""
        self.check_good_init()

        # attempt to process
        with pytest.raises(
            TypeError, match=r".*you must specify a symbolic_directory_path or stump\.*"
        ):
            self.base_pipeline.show_tree()

    def test_3(self, subtests):
        """successful usage of tree - including symbolic_directory_path and max_files"""
        self.check_good_init()

        with subtests.test(msg="main-1"):
            results = self.base_pipeline.show_tree(symbolic_directory_path="/*")
            assert results["status_code"] == 200

        with subtests.test(msg="meter-1"):
            check_meter(results, single_record=True)

        with subtests.test(msg="main-2"):
            results = self.base_pipeline.show_tree(
                symbolic_directory_path="/*", max_files=1
            )
            assert results["status_code"] == 200

        with subtests.test(msg="meter-2"):
            check_meter(results, single_record=True)

    def test_4(self):
        """success with verbose true"""
        self.check_good_init()

        result = self.show_print(symbolic_directory_path="/*", verbose=True)

        assert "value of max_files not set by user" in result["printed_output"]

    def test_5(self):
        """check using list that all symbolic_directory_paths are valid and that no inter-pipeline leaking is happening"""
        # show_tree at root stump and collect all symbolic_directory_paths
        self.check_good_init()

        tree_output_data = self.base_pipeline.show_tree(
            symbolic_directory_path="/*", verbose=False
        )
        symbolic_file_paths = tree_output_data["items"]

        # list all symbolic_directory_paths
        list_output_data = self.base_pipeline.list(
            symbolic_file_paths=symbolic_file_paths
        )
        list_items = list_output_data["items"]

        # confirm there are a at least as many list_items as there were tree symbolic_directory_paths
        assert len(list_items) == len(symbolic_file_paths)

        # confirm that each item in list_items has the correct pipeline
        for item in list_items:
            assert item["pipeline"] == self.pipeline
