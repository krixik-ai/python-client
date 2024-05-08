from tests.krixik import text_files_path
from tests.utilities.reset import reset_pipeline
from krixik import krixik
from tests import USER_API_KEY, USER_API_URL
import pytest


def test_1():
    """ test that pipeline with same name but different modules fails """
    # initialize krixik
    krixik.init(api_key=USER_API_KEY,
                api_url=USER_API_URL)

    test_file = text_files_path + "1984_very_short.txt"
    config_1 = "krixik/pipeline_examples/single_module/parser.yml"
    config_2 = "krixik/pipeline_examples/single_module/keyword-db.yml"
    
    # process with pipeline type 1
    pipeline = krixik.load_pipeline(config_path=config_1)
    pipeline.pipeline_name = "process-test-pipeline"
    reset_pipeline(pipeline)
    
    process_result = pipeline.process(local_file_path=test_file, expire_time=60*3, verbose=False)
    assert process_result["status_code"] == 200
    
    pipeline = krixik.load_pipeline(config_path=config_2)
    pipeline.pipeline_name = "process-test-pipeline"
    
    with pytest.raises(ValueError, match=r".*BAD REQUEST: you have at least one file on record with the same pipeline name\.*"):
        pipeline.process(local_file_path=test_file, expire_time=60*3, verbose=False)
    
    reset_pipeline(pipeline)