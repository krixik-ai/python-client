from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools
from tests.utilities.decorators import capture_printed_output
import pytest
import uuid


class BasePipelineStatus(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)
        self.test_data = []
        self.available_pipelines = []

    @capture_printed_output
    def show_print(self, **kwargs):
        self.base_pipeline.process_status(**kwargs)

    def test_1(self):
        """failure to status due to bad init / not first initialized"""
        self.check_bad_init()
        fake_process_id = str(uuid.uuid4())
        with pytest.raises(ValueError, match=r".*you are not authenticated\.*"):
            self.base_pipeline.process_status(request_id=fake_process_id)

    def test_2(self, file_name, local_file_path):
        self.check_good_init()
        try:
            # list file
            results = self.base_pipeline.list(file_names=[file_name])
            file_id = results["items"][0]["file_id"]

            assert results["status_code"] == 200

            # delete file
            results = self.base_pipeline.delete(file_id=file_id)

            assert results["status_code"] == 200
        except:
            pass
        finally:
            # process file
            results = self.base_pipeline.process(
                file_name=file_name, local_file_path=local_file_path
            )
            request_id = results["request_id"]

        results = self.base_pipeline.process_status(request_id=request_id)
        assert "PROCESSING COMPLETE" in results["processing_status"]

    def test_3(self):
        """failure to status due to pre-made failure process_id"""
        self.check_good_init()
        with pytest.raises(ValueError):
            results = self.base_pipeline.process_status(
                request_id="11111111-1111-1111-1111-111111111111111"
            )
