from tests.krixik.system_builder.functions.delete.utilities.setup import load_pipeline
from tests.utilities.dynamodb_interactions import check_meter
from tests.utilities.dynamodb_interactions import check_expire
from tests.utilities.scheduler_interactions import check_schedule
import pytest
import uuid


@pytest.fixture(scope="session", autouse=True)
def pipeline():
    return load_pipeline()


def test_1(pipeline):
    """failure to delete due to no input arg"""
    with pytest.raises(ValueError, match=r".*please provide a file_id\.*"):
        pipeline.delete()


def test_2(pipeline):
    """failure to delete due to non-file_id string"""
    with pytest.raises(TypeError, match=r".*invalid file_id\.*"):
        pipeline.delete(file_id="test")


def test_3(pipeline, subtests):
    """success to delete due to non-extant file_id"""
    with subtests.test(msg="delete non-extant file_id"):
        fake_file_id = str(uuid.uuid4())
        results = pipeline.delete(file_id=fake_file_id)
        assert results["status_code"] == 400

    with subtests.test(msg="meter"):
        check_meter(results)


def test_4(pipeline, subtests):
    """success with 200 status with extant file_id"""
    first_item = pipeline.list(symbolic_directory_paths=["/*"])["items"][0]
    file_id = first_item["file_id"]
    
    # check for file_id in expiration table
    assert check_expire(file_id=file_id) is True

    # check for file_id in scheduler
    assert check_schedule(file_id=file_id) is True

    # delete file
    with subtests.test(msg="delete"):
        results = pipeline.delete(file_id=file_id)
        assert results["status_code"] == 200

    with subtests.test(msg="meter-3"):
        check_meter(results)

    # attempt to list deleted file
    with subtests.test(msg="list-2"):
        results = pipeline.list(file_ids=[file_id])
        compare_file_id = results["warnings"][0][
            "WARNING: the following file_ids were not found"
        ][0].strip()
        assert file_id == compare_file_id

    assert results["status_code"] == 200

    # check for file_id in expiration table
    assert check_expire(file_id=file_id) is False

    # check for file_id in scheduler
    assert check_schedule(file_id=file_id) is False

    with subtests.test(msg="meter-4"):
        check_meter(results)


def test_5(pipeline):
    """ reset pipeline for tests """
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] == 200
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] == 200
    assert len(current_files["items"]) == 0
