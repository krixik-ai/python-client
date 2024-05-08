import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from functools import wraps
import time
from tests import USER_ID as user_id
from tests import user_stage

# import dynamodb resource
dynamodb = boto3.resource("dynamodb", region_name="us-west-2")


def convert_timestamp(timestamp_int, format="%Y-%m-%d %H:%M:%S"):
    # Convert the integer timestamp to a datetime object in UTC
    dt_object_utc = datetime.utcfromtimestamp(int(timestamp_int))

    # Format the UTC datetime object as a string
    timestamp_str_utc = dt_object_utc.strftime(format)

    return timestamp_str_utc


# remove all items from meter table
def reset_user_meter_table(user_id: str, stage: str):
    try:
        # define table name
        table_name = f"{user_id}-meter-{stage}"

        # define table resource
        table_resource = dynamodb.Table(table_name)

        # collect all items from table
        response = table_resource.scan()

        # loop over and delete all items
        for item in response["Items"]:
            table_resource.delete_item(
                Key={"meter_id": item["meter_id"], "timestamp": item["timestamp"]}
            )

        # scan table again
        response = table_resource.scan()

        # collect items
        items = response["Items"]

        # if length of items is 0, return success message
        if len(items) == 0:
            response = {"status": 200, "message": "All items removed from meter table"}
        else:
            response = {
                "status": 400,
                "message": "Failed to remove all items from meter table",
            }

        return response

    except Exception as e:
        response = {
            "status": 400,
            "message": f"Failed to remove all items from meter table: {str(e)}",
        }

        return response


# remove all items from meter table
def reset_history_table(stage: str):
    try:
        # define table name
        table_name = f"history-ledger-{stage}"

        # define table resource
        table_resource = dynamodb.Table(table_name)

        # collect all items from table
        response = table_resource.scan()

        # loop over and delete all items
        for item in response["Items"]:
            table_resource.delete_item(
                Key={"history_id": item["history_id"], "timestamp": item["timestamp"]}
            )

        # scan table again
        response = table_resource.scan()

        # collect items
        items = response["Items"]

        # if length of items is 0, return success message
        if len(items) == 0:
            response = {
                "status": 200,
                "message": "All items removed from history table",
            }
        else:
            response = {
                "status": 400,
                "message": "Failed to remove all items from history table",
            }

        return response

    except Exception as e:
        response = {
            "status": 400,
            "message": f"Failed to remove all items from history table: {str(e)}",
        }

        return response


def get_history_record(request_id: str, stage: str = user_stage):
    try:
        # formulate table name
        table_name = f"history-ledger-{stage}"

        # get table
        table = dynamodb.Table(table_name)

        # query for row with request_id - a gsi
        response = table.query(
            IndexName="RequestIdGSI",
            KeyConditionExpression="request_id = :request_id",
            ExpressionAttributeValues={":request_id": request_id},
        )

        # collect items from response
        items = response["Items"]

        # convert status to int
        for item in items:
            item["status"] = int(item["status"])

        # convert timestamp to string
        for item in items:
            item["timestamp"] = convert_timestamp(item["timestamp"])

        # convert duration to float
        for item in items:
            item["duration"] = float(item["duration"])

        return items

    except Exception as e:
        error_message = f"Failed to get history record: {str(e)}"
        return error_message


def get_meter_record(request_id: str, user_id: str, stage: str):
    try:
        # get table
        table_name = f"{user_id}-meter-{stage}"
        table = dynamodb.Table(table_name)

        # query for row with request_id - a gsi
        response = table.query(
            IndexName="RequestIdGSI",
            KeyConditionExpression="request_id = :request_id",
            ExpressionAttributeValues={":request_id": request_id},
        )

        # collect items from response
        items = response["Items"]

        # convert status to int
        for item in items:
            item["status"] = int(item["status"])

        # convert timestamp to string
        for item in items:
            item["timestamp"] = convert_timestamp(item["timestamp"])

        # convert duration to float
        for item in items:
            item["duration"] = float(item["duration"])

        return items

    except Exception as e:
        error_message = f"Failed to get meter record: {str(e)}"
        return error_message


def get_expire_record(file_id: str, stage: str):
    try:
        # get table
        table_name = f"expire-ledger-{stage}"
        table = dynamodb.Table(table_name)

        # query for row with request_id - a gsi
        response = table.query(
            IndexName="FileIdGSI",
            KeyConditionExpression="file_id = :file_id",
            ExpressionAttributeValues={":file_id": file_id},
        )

        if "Items" not in response:
            return []

        # collect items from response
        items = response["Items"]

        # convert expire_time and insert_time to int
        for item in items:
            item["insert_time"] = int(item["insert_time"])
            item["expire_time"] = int(item["expire_time"])

        return items

    except Exception as e:
        error_message = f"Failed to get expire record: {str(e)}"
        return error_message


def check_file_record(file_id: str, stage: str = user_stage):
    try:
        # construct table_name
        table_name = f"{user_id}-files-{stage}"

        # get table based on table_name
        table = dynamodb.Table(table_name)

        # get row based on file_id key
        response = table.get_item(Key={"file_id": file_id})

        # check status code of response
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("SUCCESS: get_row_by_file_id executed successfully")
            # collect item from response
            if "Item" in response:
                if len(response["Item"]) > 0:
                    return True
                return False
            return False
        else:
            print(f"FAILURE: get_row_by_file_id failed, got response: {response}")
            return False
    except ClientError as err:
        if err.response["Error"]["Code"] == "ResourceNotFoundException":
            print(
                f"SUCCESS: get_row_by_file_id failed for file_id {file_id} - got ResourceNotFoundException"
            )
            return False
    except Exception as e:
        print(
            f"FAILURE: get_row_by_file_id failed for file_id {file_id} - got exception: {e}"
        )
        return None


def check_history(results: dict, single_record: bool = True):
    # check that request_id is in results
    try:
        # get request_id from results
        request_id = results["request_id"]

        # get status from results
        results_status = results["status_code"]

        # set max_count for looking up history
        max_count = 5
        count = 0
        while count < max_count:
            # check history
            history = get_history_record(request_id, user_stage)

            # confirm length of history is 1
            if len(history) == 1:
                history_status = history[0]["status"]

                # check that status from results matches status from history
                if results_status == history_status:
                    print("SUCCESS: Status from results matches status from history")
                    return True
                else:
                    raise ValueError(
                        "Status from results does not match status from history"
                    )
            if len(history) > 1:
                if single_record:
                    raise ValueError("More than one history record found")
                else:
                    return True
            if len(history) == 0:
                count += 1
                time.sleep(2)
                continue
        raise ValueError("Failed to find history record")
    except Exception as e:
        raise ValueError(f"Failed to check history: {str(e)}")


def check_meter(results: dict, single_record: bool = True):
    try:
        # get request_id from results
        request_id = results["request_id"]

        # get status from results
        results_status = results["status_code"]

        # set max_count for looking up history
        max_count = 5
        count = 0
        while count < max_count:
            # check meter
            meter = get_meter_record(request_id, user_id, user_stage)

            # confirm length of meter is 1
            if len(meter) == 1:
                meter_status = meter[0]["status"]

                # check that status from results matches status from meter
                if results_status == meter_status:
                    print("SUCCESS: Status from results matches status from meter")
                    return True
                else:
                    raise ValueError(
                        "Status from results does not match status from meter"
                    )
            if len(meter) > 1:
                if single_record:
                    raise ValueError("More than one meter record found")
                else:
                    return True
            if len(meter) == 0:
                count += 1
                time.sleep(2)
                continue
        raise ValueError("Failed to find meter record")
    except Exception as e:
        raise ValueError(f"Failed to check meter: {str(e)}")


def check_expire(file_id: str):
    # check that file_id is in results
    try:
        # set max_count for looking up expire
        record = get_expire_record(file_id, user_stage)

        # confirm length of history is 1
        if len(record) == 1:
            print("SUCCESS: check_expire found expire record")
            return True
        print(f"SUCCESS: check_expire did not find expire record")
        return False
    except Exception as e:
        print(f"FAILURE: check_expire failed: {str(e)}")
        return None


# decorator to wrap get_meter_record and get_history_record
def check_history_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        results = func(*args, **kwargs)

        # check that request_id is in results
        try:
            # get request_id from results
            request_id = results["request_id"]

            # get status from results
            results_status = results["status_code"]

            # set max_count for looking up history
            max_count = 5
            count = 0
            while count < max_count:
                # check history
                history = get_history_record(request_id, user_stage)

                # confirm length of history is 1
                if len(history) == 1:
                    history_status = history[0]["status"]

                    # check that status from results matches status from history
                    if results_status == history_status:
                        print(
                            "SUCCESS: Status from results matches status from history"
                        )
                        return results
                    else:
                        raise ValueError(
                            "Status from results does not match status from history"
                        )
                if len(history) > 1:
                    raise ValueError("More than one history record found")
                if len(history) == 0:
                    count += 1
                    time.sleep(2)
                    continue
            raise ValueError("Failed to find history record")
        except Exception as e:
            raise ValueError(f"Failed to check history: {str(e)}")

    return wrapper


def check_meter_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        results = func(*args, **kwargs)

        # check that request_id is in results
        try:
            # get request_id from results
            request_id = results["request_id"]

            # get status from results
            results_status = results["status_code"]

            # set max_count for looking up history
            max_count = 5
            count = 0
            while count < max_count:
                # check meter
                meter = get_meter_record(request_id, user_id, user_stage)

                # confirm length of meter is 1
                if len(meter) == 1:
                    meter_status = meter[0]["status"]

                    # check that status from results matches status from meter
                    if results_status == meter_status:
                        print("SUCCESS: Status from results matches status from meter")
                        return results
                    else:
                        raise ValueError(
                            "Status from results does not match status from meter"
                        )
                if len(meter) > 1:
                    raise ValueError("More than one meter record found")
                if len(meter) == 0:
                    count += 1
                    time.sleep(2)
                    continue
            raise ValueError("Failed to find meter record")
        except Exception as e:
            raise ValueError(f"Failed to check meter: {str(e)}")

    return wrapper
