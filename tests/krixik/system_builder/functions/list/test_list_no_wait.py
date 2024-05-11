from tests.krixik.system_builder.functions.list.utilities.setup import load_but_no_process_pipeline
from tests.krixik.system_builder.functions.list.utilities.setup import output_files_path
import time


def test_1(subtests):
    """ test that list returns proper warning when using wait_for_process=False, file is not done processing, then shows success
        once file is done """

    pipeline, test_files = load_but_no_process_pipeline()
    test_file = test_files[0]
    process_output = pipeline.process(local_file_path=test_file,
                                      expire_time=60*30,
                                      modules={},
                                      local_save_directory=output_files_path,
                                      verbose=False,
                                      wait_for_process=False)
    
    api_output = pipeline.list(file_ids=[process_output["file_id"]])
    api_status = api_output["status_code"]
    api_message = api_output["message"]
    not_finished_message = "No items found for input query arguments"
    finished_message = "Successfully returned 1"
    
    with subtests.test(msg="check list message with wait_for_process as False"):
        assert api_status == 200
        assert not_finished_message in api_message
    
    with subtests.test(msg="check list for success"):
        # check for a maximum of 120 secs ever 5 seconds for proper failure_status return
        max_count = 30
        time_step = 4
        count = 0        
        api_output = pipeline.list(file_ids=[process_output["file_id"]])
        api_message = api_output["message"]
        while not_finished_message in api_message and count < max_count:
            api_output = pipeline.list(file_ids=[process_output["file_id"]])
            api_message = api_output["message"]
            time.sleep(time_step)
            count += 1
            
        assert api_output["status_code"] == 200
        assert finished_message in api_output["message"]
