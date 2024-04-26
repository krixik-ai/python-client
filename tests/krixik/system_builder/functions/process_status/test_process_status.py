from tests.krixik.system_builder.functions.process_status.utilities.setup import load_pipeline
from tests.krixik.system_builder.functions.process_status.utilities.setup import load_multi_pipeline
from tests.krixik.system_builder.functions.process_status.utilities.setup import test_data
from tests.krixik.system_builder.functions.process_status.utilities.setup import test_data_multi
from tests.krixik.system_builder.functions.process_status.utilities.test_data import test_failure_data
from tests.krixik import output_files_path
import pytest
import time


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline, subtests):
    """failure to status due to pre-made failure process_id"""
    with subtests.test(msg="main-1"):
        with pytest.raises(ValueError):
            pipeline.process_status(
                request_id="11111111-1111-1111-1111-11111111111111"
            )


def test_2(pipeline, subtests):
    """ check process status of recently processed file """
    results = pipeline.list(symbolic_directory_paths=["/*"])
    file_id = results["items"][0]["file_id"]
    process_id = results["items"][0]["process_id"]
    assert results["status_code"] == 200

    with subtests.test(msg="main-1"):
        results = pipeline.process_status(request_id=process_id)

        # assert that all values in results["process_status"] are True
        assert all(results["process_status"].values())


test_success_data = list(test_data.keys()) + list(test_data_multi.keys())

@pytest.mark.parametrize("pipeline_name", test_success_data)
def test_3(subtests, pipeline_name):
    """ check process status of file when process run in background and ensure return dict matches pipeline module chain """
    pipeilne_dict = load_multi_pipeline(pipeline_name)
    pipeline = pipeilne_dict["pipeline"]
    test_file = pipeilne_dict["test_file"]
    pipeline_ordered_modules = pipeilne_dict["pipeline_ordered_modules"]

    with subtests.test(msg="process_status expectation with successful upload"):
        output = pipeline.process(local_file_path=test_file,
                                  expire_time=60*5,
                                  modules={},
                                  local_save_directory=output_files_path,
                                  verbose=False,
                                  wait_for_process=False)

        process_status_output = pipeline.process_status(request_id=output["request_id"])
        process_status = process_status_output["process_status"]

        assert len(process_status) == len(pipeline_ordered_modules)
        assert set(process_status.keys()) == set(pipeline_ordered_modules)

    with subtests.test(msg="process_status expectation with successful upload - pipeline barrier"):
        pipeline.pipeline_name = 'my-favorite-pipeline'
        with pytest.raises(ValueError,  match=r".*pipeline of process_id does not match associated file pipeline\.*"):
            process_status_output = pipeline.process_status(request_id=output["request_id"])


def test_4(subtests):
    """ check process_status failure functionality works as expected with a purposeful ffailure  """
    pipeline_name = list(test_failure_data.keys())[0]
    test_file = test_failure_data[pipeline_name][0]["local_file_path"]
    pipeilne_dict = load_multi_pipeline(pipeline_name)
    pipeline = pipeilne_dict["pipeline"]
    
    with subtests.test(msg="process_status expectation with failed upload and wait_for_process True"):
        # catch expected error on running process with wait_for_process=True
        with pytest.raises(ValueError,  match=r".*processes associated with request_id\.*"):
            output = pipeline.process(local_file_path=test_file,
                                      expire_time=60*5,
                                      modules={"parser":{"model": "fixed", "params":{
                                        "chunk_size": 10,
                                        "overlap_size": 8
                                        }}},
                                      local_save_directory=output_files_path,
                                      verbose=False,
                                      wait_for_process=True)
        
    with subtests.test(msg="process_status expectation with failed upload and wait_for_process False"):
        # catch expected failure_status dictionary response when using wait_for_process False
        output = pipeline.process(local_file_path=test_file,
                                  expire_time=60*5,
                                  modules={"parser":{"model": "fixed", "params":{
                                    "chunk_size": 10,
                                    "overlap_size": 8
                                    }}},
                                  local_save_directory=output_files_path,
                                  verbose=False,
                                  wait_for_process=False)
        process_id = output["request_id"]
        
        # check for a maximum of 60 secs ever 5 seconds for proper failure_status return
        max_count = 15
        time_step = 4
        count = 0
        output = pipeline.process_status(request_id=process_id)
        while "failure_status" not in list(output.keys()) and count < max_count:
            output = pipeline.process_status(request_id=process_id)
            time.sleep(time_step)
            count += 1

        assert "failure_status" in list(output.keys())
        assert "failure_module" in output["failure_status"]

  
def test_end(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0