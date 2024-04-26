import boto3

# instantiate scheduler client
client = boto3.client("scheduler")


def check_schedule(file_id: str):
    """check schedule for file_id"""
    try:
        # create schedule name from file_id
        schedule_name = f"expire-schedule-{file_id}"

        # get schedule
        response = client.get_schedule(GroupName="default", Name=schedule_name)

        # assert that HTTPStatusCode is 200
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

        print(f"SUCCESS: get_schedule succeeded with for file_id {file_id}")
        return True
    except client.exceptions.ResourceNotFoundException:
        print(
            f"SUCCESS: get_schedule failed with ResourceNotFoundException for file_id {file_id}"
        )
        return False
    except Exception as e:
        print(f"FAILURE: get_schedule failed with exception {e}")
        return False
