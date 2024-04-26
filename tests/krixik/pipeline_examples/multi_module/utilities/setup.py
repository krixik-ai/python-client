
import os
from tests.krixik import output_files_path
from krixik.__base__ import library_base_dir
from tests.krixik.pipeline_examples.multi_module.utilities.test_data import test_data
from tests import TEST_DUMMY_API_KEY, TEST_DUMMY_API_URL
from krixik import krixik
krixik.init(api_key=TEST_DUMMY_API_KEY,
            api_url=TEST_DUMMY_API_URL)


def prep_pipeline_and_data(pipeline_name):
    # select first test data for each module
    test_file = test_data[pipeline_name][0]['local_file_path']
    config_path = f"{library_base_dir}/pipeline_examples/multi_module/{pipeline_name}.yml"

    # load pipeline
    pipeline = krixik.load_pipeline(config_path=config_path)
    pipeline.test_input(local_file_path=test_file)

    return pipeline, test_file


def run_test(pipeline_name):
    print('\n')
    print(f"testing {pipeline_name} with all defaults")
    
    pipeline, test_file = prep_pipeline_and_data(pipeline_name)

    # run pipeline
    output = pipeline.process(local_file_path=test_file,
                              expire_time=60*3,
                              modules={},
                              local_save_directory=output_files_path,
                              verbose=False) 

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