
import os
import copy
from tests.krixik import output_files_path
from krixik.__base__ import library_base_dir
from tests.krixik.system_builder.functions.process_status.utilities.test_data import test_data
from tests.krixik.system_builder.functions.process_status.utilities.test_data import test_data_multi
from tests.krixik.system_builder.functions.process_status.utilities.test_data import test_failure_data
from tests import USER_API_KEY, USER_API_URL
from krixik import krixik


def load_pipeline() -> object:
    # initialize krixik
    krixik.init(api_key=USER_API_KEY,
                api_url=USER_API_URL)

    # select single module pipeline and input data from test_data file
    pipeline_name = list(test_data.keys())[0]
    test_files = [v["local_file_path"] for v in test_data[pipeline_name]]
    config_path = f"{library_base_dir}/pipeline_examples/single_module/{pipeline_name}.yml"

    # construct pipeline and test all input files
    pipeline = krixik.load_pipeline(config_path=config_path)
    for test_file in test_files:
        pipeline.test_input(local_file_path=test_file)
        
    # reset the pipeline name so it is uniqe to this function
    pipeline.pipeline_name = f"{pipeline.pipeline}-process-status"
        
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
                                  expire_time=60*30,
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


def load_multi_pipeline(pipeline_name: str) -> dict:
    # initialize krixik
    krixik.init(api_key=USER_API_KEY,
                api_url=USER_API_URL)
    
    all_test_data = copy.deepcopy(test_data_multi)
    all_test_data.update(test_data)
    all_test_data.update(test_failure_data)
    
    data_keys = list(all_test_data.keys())
    if pipeline_name not in data_keys:
        raise ValueError(f"Pipeline name '{pipeline_name}' not found in test data.")

    # select single module pipeline and input data from test_data file
    test_files = [v["local_file_path"] for v in all_test_data[pipeline_name]]
    module_depth = "single_module" if pipeline_name in list(test_data.keys()) else "multi_module"
    config_path = f"{library_base_dir}/pipeline_examples/{module_depth}/{pipeline_name}.yml"


    # construct pipeline and test all input files
    pipeline = krixik.load_pipeline(config_path=config_path)
    for test_file in test_files:
        pipeline.test_input(local_file_path=test_file)
        
    # reset the pipeline name so it is uniqe to this function
    pipeline.pipeline_name = f"{pipeline.pipeline}-process-status"
    pipeline_ordered_modules = pipeline.module_chain
        
    # delete all files for pipeline before running tests
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0

    return {"pipeline": pipeline, "test_file": test_files[0], "pipeline_ordered_modules": pipeline_ordered_modules}
