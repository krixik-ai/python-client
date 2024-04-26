import time
from krixik.system_builder.functions.process import (
    get_presigned_url,
    process_local_file,
)
from krixik.tests.test_files import json_files_path
from tests.utilities.dynamodb_interactions import check_expire
from tests.utilities.scheduler_interactions import check_schedule
from tests.utilities.dynamodb_interactions import check_file_record
from tests import TEST_DUMMY_API_KEY, TEST_DUMMY_API_URL
from tests.krixik.system_builder.functions.delete.utilities.setup import load_pipeline
import pytest


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline):
    """
    after presigned url is successful, collect generated file_id and wait 60 seconds
    to ensure that auto-delete on server side is triggered.  Then make sure all traces
    of file are removed.
    """

    # fake payload_data    
    payload_data = {
        "pipeline": pipeline.pipeline,
        "pipeline_ordered_modules": pipeline.ordered_modules,
        "pipeline_output_process_keys": pipeline.pipeline_output_process_keys,
        "modules": pipeline.modules,
        "version": pipeline.version,
        "file_name": 'not_real.json',
        "symbolic_directory_path": "/etc",
        "file_tags": [],
        "file_description": "",
        "expire_time": 1800,
    }

    # create simple object to attach api_key to
    class KrixikBasePipeline:
        def __init__(self, api_key, api_url):
            self.__api_key = api_key
            self.__api_url = api_url

    # attach api_key to object
    api_object = KrixikBasePipeline(
        api_key=TEST_DUMMY_API_KEY, api_url=TEST_DUMMY_API_URL
    )

    # correctly get presigned url
    upload_check, upload_results = get_presigned_url(api_object, payload_data)

    # check that presigned url request was successful
    if not upload_check:
        assert False, "presigned url request failed"

    # unpack file_id
    file_id = upload_results["file_id"]

    # check that file_id is in user file ledger
    assert check_file_record(file_id) is True

    # check that file_id in expire ledger
    assert check_expire(file_id) is True

    # check that file_id in scheduler
    assert check_schedule(file_id) is True

    # wait 70 seconds for auto-delete to trigger
    time.sleep(70)

    # check that file_id is not in user file ledger
    assert check_file_record(file_id) is False

    # check that file_id not in expire ledger
    assert check_expire(file_id) is False

    # check that file_id not in scheduler
    assert check_schedule(file_id) is False


def test_2(pipeline):
    """
    our test - using a small file / process - to check that the auto-delete expire trigger functions as desired.
    a presigned url and file are uploaded with a short expire time.  We wait for the expire time to pass and then
    check that the file is no longer in the user file ledger, expire ledger, or scheduler.

    Note: the pipeline / model / file chosen must produce a very short process (e.g., <= 30 secs) for this test to function properly.
    """

    # fake payload_data    
    payload_data = {
        "pipeline": pipeline.pipeline,
        "pipeline_ordered_modules": pipeline.ordered_modules,
        "pipeline_output_process_keys": pipeline.pipeline_output_process_keys,
        "modules": pipeline.modules,
        "version": pipeline.version,
        "file_name": 'not_real.json',
        "symbolic_directory_path": "/etc",
        "file_tags": [],
        "file_description": "",
        "expire_time": 90,
    }

    # create simple object to attach api_key to
    class KrixikBasePipeline:
        def __init__(self, api_key, api_url):
            self.__api_key = api_key
            self.__api_url = api_url
            self.local_file_path = (
                json_files_path + "valid_1.json"
            )

    # attach api_key to object
    api_object = KrixikBasePipeline(
        api_key=TEST_DUMMY_API_KEY, api_url=TEST_DUMMY_API_URL
    )

    # correctly get presigned url
    upload_check, upload_results = get_presigned_url(api_object, payload_data)

    # check that presigned url request was successful
    if not upload_check:
        assert False, "presigned url request failed"

    # create second simple object to attach presigned_post_url_results
    class KrixikBasePipeline:
        def __init__(self):
            self.__pipeline = payload_data["pipeline"]
            self.local_file_path = (
                json_files_path + "valid_1.json"
            )
            self.__presigned_post_url_results = upload_results[
                "presigned_post_url_results"
            ]

    upload_object = KrixikBasePipeline()
    upload_object.file_id = upload_results["file_id"]
    upload_object.process_id = upload_results["request_id"]

    # process local file associated with presigned url
    upload_status_repeater_success, upload_response = process_local_file(upload_object)

    # unpack file_id
    file_id = upload_results["file_id"]

    # check that file_id is in user file ledger
    assert check_file_record(file_id) is True

    # check that file_id in expire ledger
    assert check_expire(file_id) is True

    # check that file_id in scheduler
    assert check_schedule(file_id) is True

    # wait 80 seconds for auto-delete to trigger - and not delete
    time.sleep(80)

    # check that file_id is in user file ledger
    assert check_file_record(file_id) is True

    # check that file_id in expire ledger
    assert check_expire(file_id) is True

    # check that file_id in scheduler
    assert check_schedule(file_id) is True

    # wait 40 seconds for auto-delete expire to trigger
    time.sleep(40)

    # check that file_id is not in user file ledger
    assert check_file_record(file_id) is False

    # check that file_id not in expire ledger
    assert check_expire(file_id) is False

    # check that file_id not in scheduler
    assert check_schedule(file_id) is False
