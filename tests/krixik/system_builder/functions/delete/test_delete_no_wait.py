from tests.krixik.system_builder.functions.delete.utilities.setup import load_but_no_process_pipeline
from tests.krixik.system_builder.functions.delete.utilities.setup import output_files_path
import time


def test_6(subtests):
    """ test that delete returns proper warning when using wait_for_process=False, file is not done processing, then shows success
        once file is done """

    pipeline, test_files = load_but_no_process_pipeline()
    test_file = test_files[0]
    process_output = pipeline.process(local_file_path=test_file,
                                      expire_time=60*5,
                                      modules={},
                                      local_save_directory=output_files_path,
                                      verbose=False,
                                      wait_for_process=False)
    
    delete_output = pipeline.delete(file_id=process_output["file_id"])
    delete_status = delete_output["status_code"]
    delete_message = delete_output["message"]
    not_finished_message = "The output for associated with your input file_id has not finished processing"
    finished_message = "Successfully deleted file_id"
        
    with subtests.test(msg="check delete warning with wait_for_process as False"):
        assert delete_status == 200
        assert not_finished_message in delete_message
    
    with subtests.test(msg="check delete for success"):
        # check for a maximum of 120 secs ever 5 seconds for proper failure_status return
        max_count = 30
        time_step = 4
        count = 0
        delete_output = pipeline.delete(file_id=process_output["file_id"])
        delete_message = delete_output["message"]
        while not_finished_message in delete_message and count < max_count:
            delete_output = pipeline.delete(file_id=process_output["file_id"])
            delete_message = delete_output["message"]
            time.sleep(time_step)
            count += 1
        assert delete_output["status_code"] == 200
        assert finished_message in delete_output["message"]
