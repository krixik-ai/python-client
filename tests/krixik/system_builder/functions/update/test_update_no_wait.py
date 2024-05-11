from tests.krixik.system_builder.functions.update.utilities.setup import load_but_no_process_pipeline
from tests.krixik.system_builder.functions.update.utilities.setup import output_files_path
from tests.utilities.reset import reset_pipeline
import time


def test_1(subtests):
    """ test that update returns proper warning when using wait_for_process=False, file is not done processing, then shows success
        once file is done """

    pipeline, test_files = load_but_no_process_pipeline()
    test_file = test_files[0]
    process_output = pipeline.process(local_file_path=test_file,
                                      expire_time=60*30,
                                      modules={},
                                      local_save_directory=output_files_path,
                                      verbose=False,
                                      wait_for_process=False)
    
    update_output = pipeline.update(file_id=process_output["file_id"], file_name="new_name.txt")
    update_status = update_output["status_code"]
    update_message = update_output["message"]
    not_finished_message = "The output for associated with your input file_id has not finished processing"
    finished_message = "Successfully updated file metadata"
    
    with subtests.test(msg="check update warning with wait_for_process as False"):
        assert update_status == 200
        assert not_finished_message in update_message
    
    with subtests.test(msg="check update for success"):
        # check for a maximum of 120 secs ever 5 seconds for proper failure_status return
        max_count = 30
        time_step = 4
        count = 0
        update_output = pipeline.update(file_id=process_output["file_id"], file_name="new_name.txt")
        update_message = update_output["message"]
        while not_finished_message in update_message and count < max_count:
            update_output = pipeline.update(file_id=process_output["file_id"], file_name="new_name.txt")
            update_message = update_output["message"]
            time.sleep(time_step)
            count += 1
        assert update_output["status_code"] == 200
        assert finished_message in update_output["message"]

    reset_pipeline(pipeline)
