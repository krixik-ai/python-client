import json
from typing import Dict
import requests
from krixik.system_builder.functions import cap_endpoint


def cap_check(api_key: str, api_url: str, version: str) -> dict:
    if api_key is None or api_url is None:
        raise ValueError("api_key and api_url cannot be None")

    try:
        # prep headers
        headers: Dict[str, str] = {"Content-Type": "text/plain", "krixikApiKey": api_key}
        payload_data = {"version": version, "pipeline": None, "pipeline_ordered_modules": []}

        # make post
        response = requests.post(
            (api_url or "") + cap_endpoint,
            headers=headers,
            json=payload_data,
            timeout=60,
        )
        results = json.loads(response.text)
        status_code_dict = {"status_code": response.status_code}
        status_code_dict.update(results)
        return status_code_dict
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"cap check failed with HTTPError {e}")
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(f"cap check failed with ConnectionError {e}")
    except requests.exceptions.Timeout as e:
        raise requests.exceptions.Timeout(f"cap check failed with Timeout {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"cap check failed with request exception {e}")
    except Exception as e:
        raise ValueError(f"cap check failed with request exception {e}")
