from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.dynamodb_interactions import check_history
from tests.utilities.dynamodb_interactions import check_expire
from tests.utilities.scheduler_interactions import check_schedule

import pytest
import uuid


def confirm_pipeline(items: list, target_pipeline: str):
    pipelines = [v["pipeline"] for v in items]
    assert all([v == target_pipeline for v in pipelines])


class BasePipelineDelete(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)
        self.test_data = []
        self.available_pipelines = []

    def test_1(self):
        """failure to process due to bad init / not first initialized"""
        self.check_bad_init()

        # attempt to process
        with pytest.raises(ValueError, match=r".*you are not authenticated\.*"):
            self.base_pipeline.delete(file_id=str(uuid.uuid4()))

    def test_2(self):
        """failure to delete due to no input arg"""
        self.check_good_init()
        with pytest.raises(ValueError, match=r".*please provide a file_id\.*"):
            self.base_pipeline.delete()

    def test_3(self):
        """failure to delete due to non-file_id string"""
        self.check_good_init()
        with pytest.raises(TypeError, match=r".*invalid file_id\.*"):
            self.base_pipeline.delete(file_id="test")

    def test_4(self, subtests):
        """success with to delete due to non-extant file_id"""
        self.check_good_init()
        with subtests.test(msg="main"):
            fake_file_id = str(uuid.uuid4())
            results = self.base_pipeline.delete(file_id=fake_file_id)
            assert results["status_code"] == 200

        with subtests.test(msg="meter"):
            check_meter(results, single_record=True)

    def test_5(self, file_name: str, local_file_path: str):
        """success with 200 using extant file_id"""
        try:
            # create new file to then delete
            results = self.base_pipeline.process(
                file_name=file_name, local_file_path=local_file_path
            )

            assert results["status_code"] == 200
        except:
            pass
        finally:
            # get file_id from list
            results = self.base_pipeline.list(file_names=[file_name])

            # extract file_id from results
            file_id = results["items"][0]["file_id"]

        # check for file_id in expiration table
        assert check_expire(file_id=file_id) == True

        # check for file_id in scheduler
        assert check_schedule(file_id=file_id) == True

        # delete file
        results = self.base_pipeline.delete(file_id=file_id)

        assert results["status_code"] == 200

        # attempt to list deleted file
        results = self.base_pipeline.list(file_ids=[file_id])
        compare_file_id = results["warnings"][0][
            "WARNING: the following file_ids were not found"
        ][0].strip()

        assert file_id == compare_file_id

        # check for file_id in expiration table
        assert check_expire(file_id=file_id) is False

        # check for file_id in scheduler
        assert check_schedule(file_id=file_id) is False

    def test_6(self):
        """ensure no cross-pipeline boundary deletes are allowed"""
        self.check_good_init()
        self.check_good_search_init()

        # list out first and second file
        all_items = self.list_all()
        first_file_id = all_items["items"][0]["file_id"]

        # try to update accross pipeline boundary - try to use search to delete
        update_output = self.search_pipeline.delete(file_id=first_file_id)
        assert " does not belong to pipeline" in update_output["message"]
