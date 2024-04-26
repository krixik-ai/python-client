
import os
from tests.krixik import output_files_path
from krixik.__base__ import library_base_dir
from tests.krixik.system_builder.expectations.upload_check.utilities.test_data import test_data
from tests import TEST_DUMMY_API_KEY, TEST_DUMMY_API_URL
from krixik import krixik


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
    pipeline.pipeline_name = f"{pipeline.pipeline}-upload-check"

    return pipeline
