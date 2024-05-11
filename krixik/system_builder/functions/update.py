import requests
from typing import Optional
import json
import os
from krixik.system_builder.functions import update_endpoint


def update(
    self,
    *,
    file_id: str,
    file_name: Optional[str],
    symbolic_directory_path: Optional[str],
    symbolic_file_path: Optional[str],
    file_tags: Optional[dict],
    file_description: Optional[str],
    expire_time: Optional[str],
    verbose: bool = True,
) -> dict:
    # check that file_id is not empty
    if file_id is None:
        raise ValueError("invalid file_id - file_id cannot be None")

    # check query arguments
    # check that file descriptors are not all empty
    if (
        file_name is None
        and symbolic_directory_path is None
        and symbolic_file_path is None
        and file_tags is None
        and file_description is None
        and expire_time is None
    ):
        raise ValueError(
            "at least one of the following update arguments must be given: file_name, symbolic_directory_path, symbolic_file_path, file_tags, file_description, expire_time"
        )

    # check that either file_name and symbolic_directory_path are not empty or that symbolic_file_path is not empty
    if (file_name is not None or symbolic_directory_path is not None) and symbolic_file_path is not None:
        raise ValueError("file_name and symbolic_directory_path cannot both be given if symbolic_file_path is given")

    # if symbolic_file_path is not empty, split symbolic_file_path into symbolic_directory_path and file_name
    if symbolic_file_path is not None:
        symbolic_directory_path = os.path.dirname(symbolic_file_path)
        file_name = os.path.basename(symbolic_file_path)

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
    payload_data = {
        "pipeline": pipeline,
        "version": version,
        "file_id": file_id,
        "file_name": file_name,
        "symbolic_directory_path": symbolic_directory_path,
        "file_tags": file_tags,
        "file_description": file_description,
        "expire_time": expire_time,
    }

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

    try:
        # make request
        response = requests.post(
            api_url + update_endpoint,
            headers=headers,
            json=payload_data,
            timeout=60,
        )

        # return response
        results = json.loads(response.text)
        self.request_id = results["request_id"]
        status_code_dict = {"status_code": response.status_code}
        status_code_dict.update(results)
        return status_code_dict
    except Exception as e:
        raise ValueError(f"update failed with request exception {e}")
    finally:
        self._reset_class_variables()
