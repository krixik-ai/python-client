from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.dynamodb_interactions import check_expire
from tests.utilities.scheduler_interactions import check_schedule
from tests.utilities.decorators import capture_printed_output
from krixik.utilities.validators.system import EXPIRE_TIME_DEFAULT
import pytest
import uuid
from datetime import datetime


def confirm_pipeline(items: list, target_pipeline: str):
    pipelines = [v["pipeline"] for v in items]
    assert all([v == target_pipeline for v in pipelines])


class BasePipelineUpdate(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)
        self.test_data = []
        self.available_pipelines = []

    @capture_printed_output
    def update_print(self, **kwargs):
        self.base_pipeline.update(**kwargs)

    def test_1(self, extension):
        """failure to process due to bad init / not first initialized"""
        self.check_bad_init()

        # attempt to process
        with pytest.raises(ValueError, match=r".*you are not authenticated\.*"):
            self.base_pipeline.update(
                file_id=str(uuid.uuid4()), file_name=f"this is a test.{extension}"
            )

    def test_2(self):
        """failure to delete due to no input arg"""
        self.check_good_init()
        with pytest.raises(
            ValueError, match=r".*invalid file_id - file_id cannot be None\.*"
        ):
            self.base_pipeline.update()

    def test_3(self):
        """failure to update due no update args"""
        self.check_good_init()
        with pytest.raises(
            ValueError,
            match=r".*at least one of the following update arguments must be given\.*",
        ):
            self.base_pipeline.update(file_id=str(uuid.uuid4()))

    def test_4(self, subtests, extension):
        """server side failure to update due to bad file_id"""
        self.check_good_init()
        with subtests.test(msg="main"):
            fake_file_id = str(uuid.uuid4())
            results = self.base_pipeline.update(
                file_id=fake_file_id, file_name=f"this is a test.{extension}"
            )
            assert results["status_code"] == 200

        with subtests.test(msg="meter"):
            check_meter(results, single_record=True)

    def test_5(self):
        """success with 200 error to delete due to extant file_id"""
        self.check_good_init()
        """bad overwrite update failure - cannot update a file to file_name and symbolic_directory_path of another file"""
        output = self.base_pipeline.list(max_files=2, symbolic_directory_paths=["/*"])
        first_file_id = output["items"][0]["file_id"]
        first_file_name = output["items"][0]["file_name"]
        second_file_id = output["items"][1]["file_id"]
        second_file_name = output["items"][1]["file_name"]
        second_symbolic_directory_path = output["items"][1]["symbolic_directory_path"]
        results = self.base_pipeline.update(
            file_id=first_file_id,
            file_name=second_file_name,
            symbolic_directory_path=second_symbolic_directory_path,
        )
        assert results["status_code"] == 400

    def test_6(self, file_name: str):
        """successful update of file_name"""
        self.check_good_init()

        all_items = self.list_all()

        # get first file from list
        first_file = all_items["items"][0]

        # get first_file's file_id
        first_file_id = first_file["file_id"]

        # change file_name
        results = self.base_pipeline.update(file_id=first_file_id, file_name=file_name)
        assert results["status_code"] == 200 or results["status_code"] == 400

    def test_7(self, extension):
        """successful update using mixed query arguments"""
        self.check_good_init()

        # get first item file_name and second file_id
        all_items = self.list_all()
        file_name = all_items["items"][0]["file_name"]
        file_id = all_items["items"][0]["file_id"]
        symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
        expire_time = all_items["items"][0]["expire_time"]

        # run specific update
        results = self.base_pipeline.update(
            file_id=file_id,
            file_name=f"a new file name.{extension}",
            symbolic_directory_path="/a/valid/path",
        )

        # assert results
        assert results["status_code"] == 200 or results["status_code"] == 400

        # run specific update
        results = self.base_pipeline.update(
            file_id=file_id,
            file_description="He's your Hucklberry",
            file_tags=[{"book_author": "El Twaino"}, {"book_type": "Old Timey"}],
            file_name=f"Hoockleberry Hoond.{extension}",
        )

        # assert results
        assert results["status_code"] == 200 or results["status_code"] == 400

        # run specific update
        results = self.base_pipeline.update(
            file_id=file_id, symbolic_file_path=f"/a/new/beginning/path.{extension}"
        )

        # assert results
        assert results["status_code"] == 200 or results["status_code"] == 400

        # a file_name update and an expire_time update
        results = self.base_pipeline.update(
            file_id=file_id, file_name=file_name, expire_time=EXPIRE_TIME_DEFAULT
        )

        # assert results
        assert results["status_code"] == 200 or results["status_code"] == 400

        # check for file_id in expiration table
        assert check_expire(file_id=file_id) == True

        # check for file_id in scheduler
        assert check_schedule(file_id=file_id) == True

        # check that updated expire_time is greater than original expire_time
        results = self.base_pipeline.update(
            file_id=file_id,
            file_name=f"a new file name.{extension}",
            symbolic_directory_path="/a/valid/path",
        )

        # list file_id item
        results = self.base_pipeline.list(file_ids=[file_id])["items"][0]
        updated_expire_time = results["expire_time"]

        # compare expire ties
        expire_time = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S")
        updated_expire_time = datetime.strptime(
            updated_expire_time, "%Y-%m-%d %H:%M:%S"
        )

        assert updated_expire_time > expire_time

    def test_8(self):
        """success with verbose True"""
        self.check_good_init()

        all_items = self.list_all()
        file_id = all_items["items"][0]["file_id"]

        result = self.update_print(
            file_id=file_id, file_tags=[{"NewTag": "NewTagValue"}], verbose=True
        )

        assert "lower casing file tag" in result["printed_output"]

    def test_9(self):
        """success with verbose False"""
        self.check_good_init()
        all_items = self.list_all()
        file_id = all_items["items"][0]["file_id"]

        result = self.update_print(
            file_id=file_id, file_tags=[{"NewTag": "NewTagValue"}], verbose=False
        )

        assert len(result["printed_output"]) == 0

    def test_10(self):
        """success update file_tag check: update file tags, check that
        listing and search for the file by file tag or file tag stump
        returns the file correctly
        """
        self.check_good_init()

        # list out first and second file
        all_items = self.list_all()
        first_file_id = all_items["items"][0]["file_id"]
        second_file_id = all_items["items"][1]["file_id"]

        # new file tags for first_file - these should be unique to this file and this file alone for testing purposes
        first_unique_file_tags = [
            {"unique_fake_key1": "tag1"},
            {"unique_fake_key2": "tag2"},
        ]

        second_unique_file_tags = [
            {"unique_fake_key1": "tag3"},
            {"unique_fake_key2": "tag4"},
        ]

        # update first file_id with new unique_file_tags
        result = self.update_print(
            file_id=first_file_id, file_tags=first_unique_file_tags, verbose=False
        )
        assert len(result["printed_output"]) == 0

        # update second file_id with new unique_file_tags
        result = self.update_print(
            file_id=second_file_id, file_tags=second_unique_file_tags, verbose=False
        )
        assert len(result["printed_output"]) == 0

        ## list file by explicit file_tag
        # first recover first_file_id from its first file_tag
        result = self.base_pipeline.list(file_tags=[first_unique_file_tags[0]])
        assert len(result["items"]) == 1
        assert result["items"][0]["file_id"] == first_file_id

        # second recover first_file_id from its second file_tag
        result = self.base_pipeline.list(file_tags=[first_unique_file_tags[1]])
        assert len(result["items"]) == 1
        assert result["items"][0]["file_id"] == first_file_id

        # third recover second_file_id from its first file_tag
        result = self.base_pipeline.list(file_tags=[second_unique_file_tags[0]])
        assert len(result["items"]) == 1
        assert result["items"][0]["file_id"] == second_file_id

        # fourth recover second_file_id from its second file_tag
        result = self.base_pipeline.list(file_tags=[second_unique_file_tags[1]])
        assert len(result["items"]) == 1
        assert result["items"][0]["file_id"] == second_file_id

        ## list file by file_tag stump
        # first recover both first_file_id and second_file_id via the unique_fake_key1 stump
        result = self.base_pipeline.list(file_tags=[{"unique_fake_key1": "*"}])
        assert len(result["items"]) == 2
        # collect file_ids from items
        file_ids = [item["file_id"] for item in result["items"]]
        assert first_file_id in file_ids
        assert second_file_id in file_ids

        # second recover both first_file_id and second_file_id via the unique_fake_key2 stump
        result = self.base_pipeline.list(file_tags=[{"unique_fake_key2": "*"}])
        assert len(result["items"]) == 2
        # collect file_ids from items
        file_ids = [item["file_id"] for item in result["items"]]
        assert first_file_id in file_ids
        assert second_file_id in file_ids

    def test_11(self):
        """ensure no cross-pipeline boundary updates are allowed"""
        self.check_good_init()
        self.check_good_search_init()

        # list out first and second file
        all_items = self.list_all()
        first_file_id = all_items["items"][0]["file_id"]

        # try to update accross pipeline boundary - try to use search to update
        update_output = self.search_pipeline.update(
            file_id=first_file_id, file_name="cross_boundary_update.txt"
        )
        assert "does not belong to pipeline" in update_output["message"]
