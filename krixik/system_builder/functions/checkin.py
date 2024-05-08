import json
import functools
from typing import Callable
import requests
from krixik.system_builder.functions import cli_checkin_endpoint


def checkin(api_key: str | None, api_url: str | None) -> int:
    if api_key is None or api_url is None:
        raise ValueError("api_key and api_url cannot be None")

    # prep headers
    headers: dict[str, str] = {"Content-Type": "text/plain", "krixikApiKey": api_key}

    try:
        # make request
        response = requests.post(
            api_url + cli_checkin_endpoint,
            headers=headers,
            json=json.dumps({}),
            timeout=15,
        )

        if response.status_code == 200:
            print("SUCCESS: You are now authenticated.")
            return 0
        else:
            print(f"FAILURE: You failed to authenticate - status code {response.status_code}")
            return 1
    except requests.exceptions.HTTPError as e:
        print(f"FAILURE: You failed to authenticate - HTTPError {e}")
        return 1
    except requests.exceptions.ConnectionError as e:
        print(f"FAILURE: You failed to authenticate - ConnectionError {e}")
        return 1
    except requests.exceptions.Timeout as e:
        print(f"FAILURE: You failed to authenticate - Timeout {e}")
        return 1
    except requests.exceptions.RequestException as e:
        print(f"FAILURE: You failed to authenticate - request exception {e}")
        return 1
    except Exception as e:
        print(f"FAILURE: You failed to authenticate - exception {e}")
        return 1


def check_init(self):
    if not (hasattr(self, "_KrixikBasePipeline__api_check_val") or hasattr(self, "_KrixikSearchPipeline__api_check_val")):
        raise ValueError("you are not authenticated - call init() to authenticate using your API key and url")
    else:
        if hasattr(self, "_KrixikBasePipeline__api_check_val"):
            if self._KrixikBasePipeline__api_check_val == 1:
                raise ValueError("you are not authenticated - all init() to authenticate using your API key and url")
            if self._KrixikBasePipeline__api_check_val is None:
                raise ValueError("you are not authenticated - call init() to authenticate using your API key and url")
        if hasattr(self, "_KrixikSearchPipeline__api_check_val"):
            if self._KrixikSearchPipeline__api_check_val == 1:
                raise ValueError("you are not authenticated - all init() to authenticate using your API key and url")
            if self._KrixikSearchPipeline__api_check_val is None:
                raise ValueError("you are not authenticated - call init() to authenticate using your API key and url")


def check_init_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        check_init(self)
        return func(self, *args, **kwargs)

    return wrapper
