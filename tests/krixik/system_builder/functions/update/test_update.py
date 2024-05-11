
from tests.krixik.system_builder.functions.update.utilities.setup import load_pipeline
from tests.krixik.system_builder.functions.update.utilities.setup import update_expire_time
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.dynamodb_interactions import check_expire
from tests.utilities.dynamodb_interactions import check_history
from tests.utilities.scheduler_interactions import check_schedule
from tests.utilities.reset import reset_pipeline
import pytest
import uuid
from datetime import datetime


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline):
    """failure to update due to no input arg"""
    with pytest.raises(ValueError, match=r".*invalid file_id\.*"):
        pipeline.update()
    reset_pipeline(pipeline)
        
        
def test_2(pipeline):
    """failure to update due no update args"""
    with pytest.raises(
        ValueError, match=r".*one of the following update arguments must be given:\.*"
    ):
        pipeline.update(file_id=str(uuid.uuid4()))
    reset_pipeline(pipeline)

    
def test_3(pipeline, subtests):
    """server side failure to update due to bad file_id"""
    with subtests.test(msg="fake file_id"):
        file_id = str(uuid.uuid4())
        results = pipeline.update(file_id=file_id, file_name="this is a test.json")
        assert results["status_code"] == 400

    with subtests.test(msg="meter"):
        check_meter(results)
    reset_pipeline(pipeline)


def test_4(pipeline, subtests):
    """bad overwrite update failure - cannot update a file to file_name and symbolic_directory_path of another file"""
    with subtests.test(msg="main"):
        output = pipeline.list(max_files=2, symbolic_directory_paths=["/*"])
        first_file_id = output["items"][0]["file_id"]
        first_file_name = output["items"][0]["file_name"]
        second_file_id = output["items"][1]["file_id"]
        second_file_name = output["items"][1]["file_name"]
        second_symbolic_directory_path = output["items"][1]["symbolic_directory_path"]
        results = pipeline.update(
            file_id=first_file_id,
            file_name=second_file_name,
            symbolic_directory_path=second_symbolic_directory_path,
        )
        assert results["status_code"] == 400

    with subtests.test(msg="history"):
        check_history(results)

    with subtests.test(msg="meter"):
        check_meter(results)
    reset_pipeline(pipeline)


def test_5(pipeline, subtests):
    """bad extension update failure - cannot update a file to a different extension than the one used at process"""
    with subtests.test(msg="main"):
        extensions = [".txt", ".docx", ".pdf", ".pptx"]
        output = pipeline.list(max_files=2, symbolic_directory_paths=["/*"])
        first_file_id = output["items"][0]["file_id"]
        first_file_name = output["items"][0]["file_name"]
        first_file_name_no_ext = first_file_name.split(".")[0]
        first_file_name_ext = first_file_name.split(".")[1]
        # extensions.remove("." + first_file_name_ext)
        new_file_name = first_file_name_no_ext + extensions[0]
        
        with pytest.raises(ValueError, match=r".*invalid file_name\.*"):
            pipeline.update(file_id=first_file_id, file_name=new_file_name)
    reset_pipeline(pipeline)


def test_6(pipeline, subtests):
    """successful update of file_name"""
    with subtests.test(msg="main"):
        all_items = pipeline.list(symbolic_directory_paths=["/*"])
        # get first file from list
        first_file = all_items["items"][0]

        # get first_file's file_id
        first_file_id = first_file["file_id"]

        # change file_name
        new_file_name = "not my life and twerk.json"
        results = pipeline.update(file_id=first_file_id, file_name=new_file_name)

        assert results["status_code"] == 200

    with subtests.test(msg="meter"):
        check_meter(results)
    reset_pipeline(pipeline)

        
def test_7(pipeline, subtests):
    """successful update using mixed query arguments"""
    with subtests.test(msg="main-1"):
        all_items = pipeline.list(symbolic_directory_paths=["/*"])
        file_name = all_items["items"][0]["file_name"]
        file_id = all_items["items"][0]["file_id"]
        symbolic_directory_path = all_items["items"][0]["symbolic_directory_path"]
        og_expire_time = all_items["items"][0]["expire_time"]

        # run specific update
        results = pipeline.update(
            file_id=file_id,
            file_name="a new file name.json",
            symbolic_directory_path="/a/valid/path",
        )

        # assert results
        assert results["status_code"] == 200

    with subtests.test(msg="meter-1"):
        check_meter(results)

    with subtests.test(msg="main-2"):
        # run specific update
        results = pipeline.update(
            file_id=file_id,
            file_description="He's your Hucklberry",
            file_tags=[{"book_author": "El Twaino"}, {"book_type": "Old Timey"}],
            file_name="Hoockleberry Hoond.json",
        )

        # assert results
        assert results["status_code"] == 200

    with subtests.test(msg="meter-2"):
        check_meter(results)

    with subtests.test(msg="main-3"):
        # run specific update
        results = pipeline.update(
            file_id=file_id,
            symbolic_file_path="/a/new/beginning/path.json"
        )

        # assert results
        assert results["status_code"] == 200

    with subtests.test(msg="meter-3"):
        check_meter(results)

    # check for file_id in expiration table
    assert check_expire(file_id=file_id) is True

    # check for file_id in scheduler
    assert check_schedule(file_id=file_id) is True

    # check that updated expire_time is greater than original expire_time
    results = pipeline.update(
        file_id=file_id,
        file_name="a new file name.json",
        symbolic_directory_path="/a/valid/path",
        expire_time=update_expire_time + 20,
    )

    # list file_id item
    results = pipeline.list(file_ids=[file_id])["items"][0]
    updated_expire_time = results["expire_time"]

    # convert expire_time to datetime
    og_expire_time = datetime.strptime(og_expire_time, "%Y-%m-%d %H:%M:%S")
    updated_expire_time = datetime.strptime(updated_expire_time, "%Y-%m-%d %H:%M:%S")
    assert updated_expire_time > og_expire_time

    reset_pipeline(pipeline)


def test_8(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0
    reset_pipeline(pipeline)
