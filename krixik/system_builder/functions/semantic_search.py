import json
import requests
from datetime import datetime
from typing import List
from krixik.system_builder.functions import semantic_search_endpoint

from krixik.utilities.utilities import vprint
from krixik.utilities.validators.system.base.timestamp_bookends import (
    convert_timestamps,
)
from krixik.system_builder.functions.checkin import check_init_decorator
from krixik.utilities.validators.utilities.decorators import type_check_inputs
from krixik.system_builder.utilities.decorators import kwargs_checker


@kwargs_checker
@check_init_decorator
@type_check_inputs
def semantic_search(
    self,
    *,
    query: str | None = None,
    file_ids: List | None = None,
    file_names: List | None = None,
    symbolic_directory_paths: List | None = None,
    symbolic_file_paths: List | None = None,
    file_tags: List | None = None,
    sort_order: str = "descending",
    k: int | None = None,
    max_files: int | None = None,
    created_at_start: str | None = None,
    created_at_end: str | None = None,
    last_updated_start: str | None = None,
    last_updated_end: str | None = None,
    verbose: bool = False,
) -> dict:
    """vector search over files defined by query parameters (e.g., file_ids, file_names, etc.)

    Parameters
    ----------
    query : str | None, optional
        query to search for, a string that can consist of multiple words, by default None
    file_ids : List | None, optional
        list of file_ids' files to include in the search, by default None
    file_names : List | None, optional
        list of file_names' files to include in the search, by default None
    symbolic_directory_paths : List | None, optional
        list of symbolic_directory_paths' or stumps' files to include in the search, by default None
    symbolic_file_paths : List | None, optional
        list of symbolic_file_paths' files to include in the search, by default None
    file_tags : dict | None, optional
        list of file_tags' or file_tag stumps' files to include in the search, by default None
    sort_order : str, optional
        the sort order of the files, by default "descending"
    max_files : int | None, optional
        the maximum number of files to return, by default None
    created_at_start : str | None, optional
        start date of files to include in the search, by default None
    created_at_end : str | None, optional
        end date of files to include in the search, by default None
    last_updated_start : str | None, optional
        start date of files to include in the search, by default None
    last_updated_end : str | None, optional
        end date of files to include in the search, by default None
    verbose : bool, optional
        whether to print verbose output, by default True

    Returns
    -------
    dict
        a dictionary containing the status_code, request_id, and message indicating success or failure
    """

    # check if query is empty
    if query == "" or query is None:
        raise ValueError("query is empty - please enter a query")

    # check that not all query args are None
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

    # check if k is None, if so set to default value of 5
    if k is None:
        k = 5
        vprint(
            "INFO: value of k not set by user, setting k to default value of 5.",
            verbose=verbose,
        )

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

    vprint(f"INFO: sort_order is set to {sort_order}.", verbose=verbose)

    # check timestamp bookends
    (
        created_at_start_int,
        created_at_end_int,
        last_updated_start_int,
        last_updated_end_int,
    ) = convert_timestamps(created_at_start, created_at_end, last_updated_start, last_updated_end)

    # prep payload data
    payload_data = {
        "pipeline": self._KrixikBasePipeline__pipeline,
        "pipeline_ordered_modules": self._KrixikBasePipeline__pipeline_ordered_modules,
        "query": query,
        "file_ids": file_ids,
        "file_names": file_names,
        "symbolic_directory_paths": symbolic_directory_paths,
        "symbolic_file_paths": symbolic_file_paths,
        "file_tags": file_tags,
        "k": k,
        "max_files": max_files,
        "created_at_start": created_at_start_int,
        "created_at_end": created_at_end_int,
        "last_updated_start": last_updated_start_int,
        "last_updated_end": last_updated_end_int,
    }

    # prep headers
    headers = {"Content-Type": "text/plain", "krixikApiKey": self._KrixikBasePipeline__api_key}

    # make request
    try:
        # make request
        response = requests.post(
            (self._KrixikBasePipeline__api_url or "") + semantic_search_endpoint,
            headers=headers,
            json=payload_data,
            timeout=60,
        )

        # return response
        results = json.loads(response.text)
        # self.request_id = results['request_id']
        status_code_dict = {"status_code": response.status_code}
        if response.status_code == 200:
            if sort_order == "global":
                global_items = []
                # create separate entry for each file_id
                for item in results["items"]:
                    # get file_id
                    vector_file_id = item["file_id"]

                    # get file_name
                    vector_file_name = item["file_metadata"]["file_name"]

                    # get symbolic_directory_path
                    vector_symbolic_directory_path = item["file_metadata"]["symbolic_directory_path"]

                    # get file_tags
                    vector_file_tags = item["file_metadata"]["file_tags"]

                    # get num_lines
                    vector_num_lines = item["file_metadata"]["num_lines"] if "num_lines" in item["file_metadata"] else 0

                    # get created_at
                    vector_created_at = item["file_metadata"]["created_at"]

                    # get last_updated
                    vector_last_updated = item["file_metadata"]["last_updated"]

                    # get search_results
                    vector_search_results = item["search_results"]

                    # create new simplified entry for each search result
                    for s in vector_search_results:
                        # unpack search result
                        snippet = s["snippet"]
                        distance = s["distance"]
                        line_numbers = s["line_numbers"]

                        # pack new_s
                        new_s = {}
                        new_s["snippet"] = snippet
                        new_s["distance"] = distance
                        new_s["line_numbers"] = line_numbers

                        file_metadata = {}
                        file_metadata["file_id"] = vector_file_id
                        file_metadata["file_name"] = vector_file_name
                        file_metadata["symbolic_directory_path"] = vector_symbolic_directory_path
                        file_metadata["file_tags"] = vector_file_tags
                        file_metadata["num_lines"] = vector_num_lines
                        file_metadata["created_at"] = vector_created_at
                        file_metadata["last_updated"] = vector_last_updated

                        new_s["file_metadata"] = file_metadata

                        # add simple_search_result to global_normalized_enriched_vector_search_results
                        global_items.append(new_s)

                # sort global_normalized_enriched_vector_search_results by distance
                results["items"] = sorted(global_items, key=lambda x: x["distance"])

            if sort_order == "descending":
                # sort user_items based on created_at
                results["items"] = sorted(
                    results["items"],
                    key=lambda x: datetime.strptime(x["file_metadata"]["created_at"], "%Y-%m-%d %H:%M:%S").timestamp(),
                    reverse=True,
                )

            if sort_order == "ascending":
                # sort user_items based on created_at
                results["items"] = sorted(
                    results["items"],
                    key=lambda x: datetime.strptime(x["file_metadata"]["created_at"], "%Y-%m-%d %H:%M:%S").timestamp(),
                    reverse=False,
                )

        status_code_dict.update(results)
        return status_code_dict
    except Exception as e:
        raise ValueError(f"vector search failed with request exception {e}") from e
