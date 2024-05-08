import requests
import json
from krixik.utilities.tree_illustrator import show_symbolic_file_tree
from krixik.system_builder.functions import show_tree_endpoint
from krixik.utilities.utilities import vprint


def show_post(self, *, symbolic_directory_path: str, max_files: int = 1000, verbose: bool = True):
    if hasattr(self, "_KrixikBasePipeline__version"):
        version = self._KrixikBasePipeline__version
    elif hasattr(self, "_KrixikSearchPipeline__version"):
        version = self._KrixikSearchPipeline__version
    else:
        raise ValueError("version not found in self")

    try:
        if hasattr(self, "_KrixikBasePipeline__api_key") and hasattr(self, "_KrixikBasePipeline__api_url"):
            api_key = self._KrixikBasePipeline__api_key
            api_url = self._KrixikBasePipeline__api_url
        else:
            raise ValueError("api_key and api_url not found in self")

        if not hasattr(self, "_KrixikBasePipeline__pipeline"):
            raise ValueError("pipeline not found in input object")

        if symbolic_directory_path is None:
            raise TypeError("you must specify a symbolic_directory_path or stump")

        # prep headers
        headers = {"Content-Type": "text/plain", "krixikApiKey": api_key}

        # prep payload data
        payload_data = {
            "pipeline": self._KrixikBasePipeline__pipeline,
            "symbolic_directory_path": symbolic_directory_path,
            "max_files": max_files,
            "version": version,
        }

        # make request
        response = requests.post(
            api_url + show_tree_endpoint,
            headers=headers,
            json=payload_data,
            timeout=60,
        )

        # unpack response
        results = json.loads(response.text)
        self.request_id = results["request_id"]
        if response.status_code == 200 or response.status_code == 400:
            status_code_dict = {"status_code": response.status_code}
            status_code_dict.update(results)
            return status_code_dict
        else:
            raise ValueError(f"show_tree failed with status code {response.status_code}")
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"show_tree failed with HTTPError {e}")
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(f"show_tree failed with ConnectionError {e}")
    except requests.exceptions.Timeout as e:
        raise requests.exceptions.Timeout(f"show_tree failed with Timeout {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"show_tree failed with request exception {e}")
    except Exception as e:
        raise ValueError(f"show_tree failed with request exception {e}")
    finally:
        self._reset_class_variables()


def show_illustration(self, *, results: dict):
    try:
        # unpack items
        items = results["items"]

        # show paths if items is not None
        if items is not None:
            show_symbolic_file_tree(items)
        else:
            print("no items to show")
    except Exception as e:
        raise ValueError(f"show_tree failed with request exception {e}")
