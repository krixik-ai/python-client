from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.decorators import capture_printed_output
import pytest


class BasePipelineProcess(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)
        self.test_data = []
        self.available_pipelines = []

    @capture_printed_output
    def upload_print(self, **kwargs):
        self.base_pipeline.process(**kwargs)

    def test_1(self, file_name: str, local_file_path: str):
        """failure to process due to bad init / not first initialized"""
        self.check_bad_init()

        # attempt to process
        with pytest.raises(ValueError, match=r".*you are not authenticated\.*"):
            self.base_pipeline.process(
                file_name=file_name, local_file_path=local_file_path
            )

    def test_2(self, local_file_path: str):
        """`process succeed when no `file_name` is given."""
        self.check_good_init()
        output_data = self.base_pipeline.process(local_file_path=local_file_path)
        assert output_data["status_code"] == 200

    def test_3(self, file_name: str):
        """`process` fails client-side when null `local_file_path` used."""
        self.check_good_init()
        with pytest.raises(ValueError, match=r".*local_file_path\.*"):
            self.base_pipeline.process(file_name=file_name)

    def test_4(self, subtests, file_name: str, local_file_path: str):
        """`that `process` succeeds with proper input arguments."""
        self.check_good_init()
        file_output_data = self.base_pipeline.process(
            file_name=file_name,
            local_file_path=local_file_path,
            symbolic_directory_path="/home/books/nonfiction/biographies",
            file_tags=[
                {"century": "19th"},
                {"book_category": "nonfiction"},
                {"book_author": "ford"},
                {"book_title": "my_life_and_work"},
            ],
            file_description="Full text of My Life and Work by Henry Ford.",
            verbose=True,
        )

        # assert status code 200
        assert file_output_data["status_code"] == 200

        # check that record can be found in user meter table
        with subtests.test(msg="meter-1"):
            check_meter(file_output_data, single_record=False)

    def test_5(self, file_name: str, local_file_path: str):
        """check that `process` fails when uploading the same `file_name` and `symbolic_directory_path`."""
        self.check_good_init()
        with pytest.raises(ValueError, match=r".*already exists\.*"):
            self.base_pipeline.process(
                file_name=file_name,
                local_file_path=local_file_path,
                symbolic_directory_path="/home/books/nonfiction/biographies",
            )

    def test_6(self, subtests, symbolic_file_path: str, local_file_path: str):
        """check that `process` succeeds when using symbolic_file_path"""
        self.check_good_init()

        with subtests.test(msg="main-1"):
            file_output_data = self.base_pipeline.process(
                local_file_path=local_file_path,
                symbolic_file_path=symbolic_file_path,
                file_tags=[
                    {"century": "who knows"},
                    {"book_category": "nonfiction"},
                    {"book_author": "ford"},
                    {"book_title": "my_life_and_work"},
                ],
            )

            # assert status code 200
            assert file_output_data["status_code"] == 200

        with subtests.test(msg="meter-1"):
            check_meter(file_output_data, single_record=False)

    def test_7(self, file_name: str, local_file_path: str, modules: str):
        """check that `process` succeeds with all current modules variations"""
        self.check_good_init()
        file_output_data = self.base_pipeline.process(
            file_name=file_name, local_file_path=local_file_path, modules=modules
        )
        assert file_output_data["status_code"] == 200

    def test_8(self, file_name: str, local_file_path: str):
        """test that process with and with verbose True"""
        self.check_good_init()
        result = self.upload_print(
            file_name=file_name, local_file_path=local_file_path, verbose=True
        )

        assert "input and output processing complete" in result["printed_output"]

    def test_9(self, file_name: str, local_file_path: str):
        """test that process verbose False does not print anything to the console"""
        self.check_good_init()
        result = self.upload_print(
            file_name=file_name, local_file_path=local_file_path, verbose=False
        )
        assert len(result["printed_output"]) == 0

    def test_10(self, file_name: str, local_file_path: str):
        """`.process` fails client-side when no `file_name` and `local_file_path` are have different extensions."""
        self.check_good_init()
        with pytest.raises(
            ValueError,
            match=r".*file_name and local_file_path must have the same extension\.*",
        ):
            self.base_pipeline.process(
                file_name=file_name, local_file_path=local_file_path
            )
