import json
from typing import Dict, Any
import requests
import time
from krixik.system_builder.functions import upload_status_endpoint
from krixik.utilities.utilities import vprint


def process_status_reporter(
    self,
    prev_process_status: dict | str | None,
    process_status: dict | str | None,
    verbose: bool,
) -> bool:
    if process_status is None or (isinstance(process_status, str)):
        raise ValueError(f"file process failed - the request_id of this failed process is {self.process_id}")

    # loop through og_process_status and check if any processing_complete is True
    module_count = 1
    for key, value in process_status.items():
        if process_status[key]:
            if prev_process_status is None or not prev_process_status[key]:
                vprint(
                    f"SUCCESS: module {module_count} (of {len(process_status)}) - {key.split('.')[0]} processing complete.",
                    verbose=verbose,
                )
        module_count += 1
    # if all values in process_status are True, then process is complete
    values = list(process_status.values())
    process_complete = True
    if not all(values):
        process_complete = False

    return process_complete


def check_process_status(self, *, process_id: str) -> tuple:
    max_count = 9
    start_count = 0
    backoff_schedule = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    while start_count < max_count:
        try:
            if process_id is None:
                raise ValueError("process_id cannot be none when checking process_status")

            if hasattr(self, "_KrixikBasePipeline__pipeline"):
                pipeline = self._KrixikBasePipeline__pipeline
            elif hasattr(self, "_KrixikSearchPipeline__pipeline"):
                pipeline = self._KrixikSearchPipeline__pipeline
            else:
                raise ValueError("pipeline not found in self")

            if hasattr(self, "_KrixikBasePipeline__version"):
                version = self._KrixikBasePipeline__version
            elif hasattr(self, "_KrixikSearchPipeline__version"):
                version = self._KrixikSearchPipeline__version
            else:
                raise ValueError("version not found in self")

            # prep payload data
            payload_data: Dict[str, str] = {
                "pipeline": pipeline,
                "version": version,
                "process_id": process_id,
            }

            if hasattr(self, "_KrixikBasePipeline__api_key") and hasattr(self, "_KrixikBasePipeline__api_url"):
                api_key = self._KrixikBasePipeline__api_key
                api_url = self._KrixikBasePipeline__api_url
            elif hasattr(self, "_KrixikSearchPipeline__api_key") and hasattr(self, "_KrixikSearchPipeline__api_url"):
                api_key = self._KrixikSearchPipeline__api_key
                api_url = self._KrixikSearchPipeline__api_url
            else:
                raise ValueError("api_key and api_url not found in self")

            # prep headers - type hint correctly
            headers: Dict[str, str] = {
                "Content-Type": "text/plain",
                "krixikApiKey": api_key or "",
            }

            # make request
            response: requests.Response = requests.post(
                (api_url or "") + upload_status_endpoint,
                headers=headers,
                json=payload_data,
                timeout=300,
            )

            # unpack response
            response_text = json.loads(response.text)
            self.request_id = response_text["request_id"]

            # Check the response
            if response.status_code == 200:
                file_id = response_text["file_id"]
                process_status: Dict[str, Any] = json.loads(response.text)["process_status"]

                failure_status: Any = response_text["failure_status"]
                message = response_text["message"]
                return file_id, process_status, failure_status, message
            else:
                message = response_text["message"]
                raise ValueError(
                    f"request failed with status code: {response.status_code} - the request_id of this failed status check is {self.request_id} - this request failed with the following message from the server: {message}"
                )
        except ValueError as err:
            raise err
        except requests.exceptions.ConnectionError as e:
            if start_count < max_count:
                time.sleep(backoff_schedule[start_count])
                start_count += 1
                continue
            raise requests.exceptions.ConnectionError(
                f"request failed with ConnectionError {e} - the request_id of this failed status check is {self.request_id}"
            )
        except requests.exceptions.Timeout as e:
            if start_count < max_count:
                time.sleep(backoff_schedule[start_count])
                start_count += 1
                continue
            raise requests.exceptions.Timeout(f"request failed with Timeout {e} - the request_id of this failed status check is {self.request_id}")
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"request failed with request exception {e} - the request_id of this failed status check is {self.request_id}"
            )
