import json
import requests
from krixik.system_builder.functions import upload_presigned_endpoint
from krixik.system_builder.functions.delete import delete_server_files


def process_local_file(self) -> tuple[bool, requests.Response]:
    if hasattr(self, "_KrixikBasePipeline__presigned_post_url_results"):
        if self._KrixikBasePipeline__presigned_post_url_results is None:
            raise ValueError("presigned_post_url_results is None - cannot upload file for processing")
        if "url" not in self._KrixikBasePipeline__presigned_post_url_results:
            raise ValueError("key 'url' not in presigned_post_url_data")
        if "fields" not in self._KrixikBasePipeline__presigned_post_url_results:
            raise ValueError("key 'fields' not in presigned_post_url_data")
        url = self._KrixikBasePipeline__presigned_post_url_results["url"]
        fields = self._KrixikBasePipeline__presigned_post_url_results["fields"]
    elif hasattr(self, "_KrixikSearchPipeline__presigned_post_url_results"):
        if self._KrixikSearchPipeline__presigned_post_url_results is None:
            raise ValueError("presigned_post_url_results is None - cannot upload file for processing")
        if "url" not in self._KrixikSearchPipeline__presigned_post_url_results:
            raise ValueError("key 'url' not in presigned_post_url_data")
        if "fields" not in self._KrixikSearchPipeline__presigned_post_url_results:
            raise ValueError("key 'fields' not in presigned_post_url_data")
        url = self._KrixikSearchPipeline__presigned_post_url_results["url"]
        fields = self._KrixikSearchPipeline__presigned_post_url_results["fields"]
    else:
        raise ValueError("presigned_post_url_results is not in self - cannot upload file for processing")

    upload_response_success = False
    try:
        if self.local_file_path is None:
            raise ValueError("local_file_path is None - cannot upload file for processing")

        # open file as binary and attempt post to s3
        with open(self.local_file_path, "rb") as f:
            files = {"file": (self.local_file_path, f)}
            upload_response = requests.post(url, data=fields, files=files, timeout=45)
            upload_response_success = True
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"local file upload request with upload request_id {self.process_id} failed with HTTPError {e}")
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(
            f"local file upload request with upload request_id {self.process_id} failed with ConnectionError {e}"
        )
    except requests.exceptions.Timeout as e:
        raise requests.exceptions.Timeout(f"local file upload request with upload request_id {self.process_id} failed with Timeout {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"local file upload request with upload request_id {self.process_id} failed with request exception {e}"
        )
    except Exception as e:
        raise Exception(f"local file upload request with upload request_id {self.process_id} failed with exception {e}")
    finally:
        if not upload_response_success:
            delete_server_files(self)
    return upload_response_success, upload_response


def get_presigned_url(self, payload_data):
    try:
        if hasattr(self, "_KrixikBasePipeline__api_key") and hasattr(self, "_KrixikBasePipeline__api_url"):
            api_key = self._KrixikBasePipeline__api_key
            api_url = self._KrixikBasePipeline__api_url
        elif hasattr(self, "_KrixikSearchPipeline__api_key") and hasattr(self, "_KrixikSearchPipeline__api_url"):
            api_key = self._KrixikSearchPipeline__api_key
            api_url = self._KrixikSearchPipeline__api_url
        else:
            raise ValueError("api_key and api_url not found in self")

        # prep headers
        headers = {"Content-Type": "text/plain", "krixikApiKey": api_key}

        # make request
        response = requests.post(
            api_url + upload_presigned_endpoint,
            headers=headers,
            json=payload_data,
            timeout=15,
        )
        result = json.loads(response.text)

        if response.status_code == 200:
            return True, result
        if response.status_code == 400:
            return False, result
        if response.status_code == 500:
            raise requests.exceptions.HTTPError("FAILURE: request check in failed with status code 500")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            raise ValueError(json.loads(e.response.text)["message"])
        else:
            raise requests.exceptions.HTTPError(f"request failed with HTTPError {e}")
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(f"request failed with ConnectionError {e}")
    except requests.exceptions.Timeout as e:
        raise requests.exceptions.Timeout(f"request failed with Timeout {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"request failed with request exception {e}")
    except Exception as e:
        raise Exception(f"request failed with exception {e}")
