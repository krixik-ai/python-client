
import os
import yaml
from tests.krixik import output_files_path
from krixik.__base__ import library_base_dir
from tests.krixik.pipeline_examples.single_module.utilities.test_data import module_test_data
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.dynamodb_interactions import check_expire
from tests.utilities.scheduler_interactions import check_schedule
from tests.utilities.dynamodb_interactions import check_cap

from tests import USER_API_KEY, USER_API_URL, USER_ID
from krixik import krixik
krixik.init(api_key=USER_API_KEY,
            api_url=USER_API_URL)


def get_available_models(module_name):
    config_path = f"{library_base_dir}/pipeline_examples/single_module/{module_name}.yml"
    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    available_models = []
    for v in config["pipeline"]["modules"][0]["models"]:
        model = v["name"]
        params = {}
        if "params" in list(v.keys()):
            ordered_params = dict(v["params"])
            param_keys = list(ordered_params.keys())
            for p in param_keys:
                params[p] = ordered_params[p]["default"]
        entry = {}
        entry["model"] = model
        entry["params"] = params
        available_models.append(entry)
    return available_models


def prep_pipeline_and_data(module_name):
    # select first test data for each module
    test_file = module_test_data[module_name][0]['local_file_path']
    config_path = f"{library_base_dir}/pipeline_examples/single_module/{module_name}.yml"

    # load pipeline
    pipeline = krixik.load_pipeline(config_path=config_path)
    pipeline.test_input(local_file_path=test_file)
    available_models = get_available_models(module_name)

    return [(pipeline, test_file, v) for v in available_models]


def run_test(module_name, module_selection, pipeline, test_file):    
    print('\n')
    print(f"testing {module_name} with model {module_selection}")
    
    original_cap_record = check_cap(USER_ID)
    original_units_used = int(original_cap_record["units_used"])

    # run pipeline
    output = pipeline.process(local_file_path=test_file,
                              expire_time=60*30,
                              modules={module_name: module_selection},
                              local_save_directory=output_files_path,
                              verbose=False) 

    # assert 200 status code
    assert output["status_code"] == 200
    
    # check meter
    assert check_meter(output) is True
    
    # check cap 
    follow_cap_record = check_cap(USER_ID)
    follow_units_used = int(follow_cap_record["units_used"])
    assert follow_units_used - original_units_used > 0
    
    # check for file_id in expiration table
    assert check_expire(file_id=output["file_id"]) is True

    # check for file_id in scheduler
    assert check_schedule(file_id=output["file_id"]) is True

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