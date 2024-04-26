
import os
from tests.krixik import output_files_path
from krixik.__base__ import library_base_dir
from tests.krixik.system_builder.functions.update.utilities.test_data import test_data
from tests.krixik.system_builder.functions.update.utilities.test_data import wait_for_test_data

from tests import TEST_DUMMY_API_KEY, TEST_DUMMY_API_URL
from krixik import krixik


# define expire time
update_expire_time = 60*5


def load_but_no_process_pipeline():
    # initialize krixik
    krixik.init(api_key=TEST_DUMMY_API_KEY,
                api_url=TEST_DUMMY_API_URL)

    pipeline_name = list(wait_for_test_data.keys())[0]
    test_files = [v["local_file_path"] for v in wait_for_test_data[pipeline_name]]
    config_path = f"{library_base_dir}/pipeline_examples/multi_module/{pipeline_name}.yml"

    # construct pipeline and test all input files
    pipeline = krixik.load_pipeline(config_path=config_path)
    for test_file in test_files:
        pipeline.test_input(local_file_path=test_file)
        
    # reset the pipeline name so it is uniqe to this function
    pipeline.pipeline_name = f"{pipeline.pipeline}-update"
        
    # delete all files for pipeline before running tests
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0

    return pipeline, test_files


def load_pipeline():
    # initialize krixik
    krixik.init(api_key=TEST_DUMMY_API_KEY,
                api_url=TEST_DUMMY_API_URL)

    # select single module pipeline and input data from test_data file
    pipeline_name = list(test_data.keys())[0]
    test_files = [v["local_file_path"] for v in test_data[pipeline_name]]
    config_path = f"{library_base_dir}/pipeline_examples/single_module/{pipeline_name}.yml"

    # construct pipeline and test all input files
    pipeline = krixik.load_pipeline(config_path=config_path)
    for test_file in test_files:
        pipeline.test_input(local_file_path=test_file)
        
    # reset the pipeline name so it is uniqe to this function
    pipeline.pipeline_name = f"{pipeline.pipeline}-update"
        
    # delete all files for pipeline before running tests
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0

    # process all input files
    for ind, test_file in enumerate(test_files):
        output = pipeline.process(local_file_path=test_file,
                                expire_time=update_expire_time,
                                modules={},
                                local_save_directory=output_files_path,
                                verbose=False,
                                symbolic_directory_path="/home",
                                file_tags=[
                                    {"book_category": "nonfiction"},
                                    {"book_author": "ford"},
                                    {"book_title": "my_life_and_work"}])

        # assert 200 status code
        assert output["status_code"] == 200

        # check that output is a dictionary
        process_output_files = output["process_output_files"]

        # assert that each element of process_output_files represents a real file
        for file in process_output_files:
            assert os.path.isfile(file)

        # delete output files
        for file in process_output_files:
            os.remove(file)

        # assert that all output files have been deleted
        for file in process_output_files:
            assert not os.path.isfile(file)
    return pipeline