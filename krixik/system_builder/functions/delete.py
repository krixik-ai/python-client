import json
import requests
from krixik.system_builder.functions import delete_endpoint


def delete_server_files(self) -> dict:
    try:
        if self.file_id is None:
            raise ValueError("file_id is None - please provide a file_id")

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

        payload_data = {
            "pipeline": pipeline,
            "version": version,
            "file_id": self.file_id,
        }

        if hasattr(self, "_KrixikBasePipeline__api_key") and hasattr(self, "_KrixikBasePipeline__api_url"):
            api_key = self._KrixikBasePipeline__api_key
            api_url = self._KrixikBasePipeline__api_url
        elif hasattr(self, "_KrixikSearchPipeline__api_key") and hasattr(self, "_KrixikSearchPipeline__api_url"):
            api_key = self._KrixikSearchPipeline__api_key
            api_url = self._KrixikSearchPipeline__api_url
        else:
            raise ValueError("api_key and api_url not found in self")

        headers = {"Content-Type": "text/plain", "krixikApiKey": api_key}

        response = requests.post(
            (api_url or "") + delete_endpoint,
            headers=headers,
            json=payload_data,
            timeout=60,
        )

        response_text = json.loads(response.text)
        self.request_id = response_text["request_id"]

        results = json.loads(response.text)
        status_code_dict = {"status_code": response.status_code}
        status_code_dict.update(results)
        return status_code_dict
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"delete failed with HTTPError {e}")
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(f"delete failed with ConnectionError {e}")
    except requests.exceptions.Timeout as e:
        raise requests.exceptions.Timeout(f"delete failed with Timeout {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"delete failed with request exception {e}")
    except Exception as e:
        raise ValueError(f"delete failed with request exception {e}")
    finally:
        self._reset_class_variables()
