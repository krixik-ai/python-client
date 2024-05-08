import os
import json
import requests
from krixik.system_builder.functions import fetch_output_endpoint


def download_file(url, save_path):
    try:
        with requests.get(url, timeout=60) as r:
            r.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"download_file failed with HTTPError exception: {e}")


def save_output(url: str, file_id: str, extension: str, output_save_directory: str) -> str:
    save_path = f"{output_save_directory}/{file_id}{extension}"
    download_file(url, save_path)
    return save_path


def fetch_output(self, file_id: str, local_save_directory: str) -> dict | None:
    if file_id is None:
        raise ValueError("please provide a file_id")
    if not os.path.exists(local_save_directory):
        raise ValueError(f"local_save_directory {local_save_directory} does not exist")
    if not os.access(local_save_directory, os.W_OK):
        raise ValueError(f"local_save_directory {local_save_directory} is not writeable")
    if not os.access(local_save_directory, os.R_OK):
        raise ValueError(f"local_save_directory {local_save_directory} is not readable")

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
            (api_url or "") + fetch_output_endpoint,
            headers=headers,
            json=payload_data,
            timeout=60,
        )

        # return response
        results = json.loads(response.text)
        process_output = results["process_output"]
        if process_output is not None:
            save_paths = []
            for output in process_output:
                save_path = save_output(
                    output["url"],
                    file_id,
                    output["extension"],
                    local_save_directory,
                )
                save_paths.append(save_path)

            results["process_output_files"] = save_paths
            results["message"] += "Output saved to location(s) listed in process_output_files."
            if len(process_output) == 1:
                if process_output[0]["extension"] == ".json":
                    with open(save_paths[0], "r") as file:
                        results["process_output"] = json.load(file)
                else:
                    results["process_output"] = None
            else:
                results["process_output"] = None
        status_code_dict = {"status_code": response.status_code}
        status_code_dict.update(results)
        return status_code_dict
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"FAILURE: fetch_output failed with HTTPError exception: {e}")
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(f"FAILURE: fetch_output failed with ConnectionError exception: {e}")
    except requests.exceptions.Timeout as e:
        raise requests.exceptions.Timeout(f"FAILURE: fetch_output failed with Timeout exception: {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"FAILURE: fetch_output failed with RequestException exception: {e}")
    except Exception as e:
        ValueError(f"FAILURE: fetch_output failed with general exception: {e}")
    finally:
        self._reset_class_variables()
