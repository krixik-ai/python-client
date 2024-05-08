import requests
import json
import datetime
from krixik.utilities.utilities import vprint
from krixik.utilities.validators.system.base.timestamp_bookends import (
    convert_timestamps,
)
from krixik.system_builder.functions import list_endpoint


# method for listing files
def list_files(
    self,
    *,
    file_ids: list | None = None,
    file_names: list | None = None,
    symbolic_directory_paths: list | None = None,
    symbolic_file_paths: list | None = None,
    file_tags: list | None = None,
    sort_order: str = "descending",
    max_files: int | None = None,
    created_at_start: str | None = None,
    created_at_end: str | None = None,
    last_updated_start: str | None = None,
    last_updated_end: str | None = None,
    verbose: bool = True,
) -> dict:
    # check that at least one query argument is given
    if (
        file_ids is None
        and file_names is None
        and symbolic_directory_paths is None
        and symbolic_file_paths is None
        and file_tags is None
        and created_at_start is None
        and created_at_end is None
        and last_updated_start is None
        and last_updated_end is None
    ):
        raise ValueError("please provide at least one query argument")

    # if max_files is None, set to default value of 1000
    if max_files is None:
        max_files = 1000
        vprint(
            "INFO: value of max_files not set by user, setting max_files to default value of 1000.",
            verbose=verbose,
        )

    if sort_order is None:
        sort_order = "descending"
        vprint(
            "INFO: value of sort_order not set by user, setting sort_order to default value of descending.",
            verbose=verbose,
        )
    else:
        vprint(f"INFO: sort_order set to {sort_order}", verbose=verbose)

    # check timestamp bookends
    (
        created_at_start_int,
        created_at_end_int,
        last_updated_start_int,
        last_updated_end_int,
    ) = convert_timestamps(created_at_start, created_at_end, last_updated_start, last_updated_end)

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
        "file_ids": file_ids,
        "file_names": file_names,
        "symbolic_directory_paths": symbolic_directory_paths,
        "symbolic_file_paths": symbolic_file_paths,
        "file_tags": file_tags,
        "max_files": max_files,
        "created_at_start": created_at_start_int,
        "created_at_end": created_at_end_int,
        "last_updated_start": last_updated_start_int,
        "last_updated_end": last_updated_end_int,
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
        response = requests.post(api_url + list_endpoint, headers=headers, json=payload_data, timeout=60)

        # return response
        results = json.loads(response.text)
        if "request_id" in results:
            self.request_id = results["request_id"]
        status_code_dict = {"status_code": response.status_code}
        if response.status_code == 200:
            if sort_order == "descending":
                # sort user_items based on created_at
                results["items"] = sorted(
                    results["items"],
                    key=lambda x: datetime.datetime.strptime(x["created_at"], "%Y-%m-%d %H:%M:%S").timestamp(),
                    reverse=True,
                )
            elif sort_order == "ascending":
                # sort user_items based on created_at
                results["items"] = sorted(
                    results["items"],
                    key=lambda x: datetime.datetime.strptime(x["created_at"], "%Y-%m-%d %H:%M:%S").timestamp(),
                    reverse=False,
                )
        status_code_dict.update(results)
        return status_code_dict
    except Exception as e:
        raise ValueError(f"list failed with request exception {e}")
    finally:
        self._reset_class_variables()
